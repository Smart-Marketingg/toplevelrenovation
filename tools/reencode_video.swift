// Re-encode a reel with macOS AVFoundation (no ffmpeg needed). Drops audio.
// swiftc -O tools/reencode_video.swift -o /tmp/reencode
// /tmp/reencode in.mp4 video/reel-x.mp4 360 640 900000
import AVFoundation

// usage: reencode <in.mp4> <out.mp4> <width> <height> <bitsPerSecond>
let a = CommandLine.arguments
let src = URL(fileURLWithPath: a[1]), dst = URL(fileURLWithPath: a[2])
let W = Int(a[3])!, H = Int(a[4])!, BPS = Int(a[5])!
try? FileManager.default.removeItem(at: dst)

let asset = AVURLAsset(url: src)
let sema = DispatchSemaphore(value: 0)
var track: AVAssetTrack!
var fps: Float = 30
Task {
    track = try! await asset.loadTracks(withMediaType: .video).first!
    fps = try! await track.load(.nominalFrameRate)
    sema.signal()
}
sema.wait()

let reader = try! AVAssetReader(asset: asset)
let out = AVAssetReaderTrackOutput(track: track, outputSettings: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange])
out.alwaysCopiesSampleData = false
reader.add(out)

let writer = try! AVAssetWriter(outputURL: dst, fileType: .mp4)
writer.shouldOptimizeForNetworkUse = true   // moov atom first, so playback starts before the whole file loads
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W, AVVideoHeightKey: H,
    AVVideoScalingModeKey: AVVideoScalingModeResizeAspectFill,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: BPS,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoMaxKeyFrameIntervalKey: Int(fps.rounded()) * 2,
        AVVideoExpectedSourceFrameRateKey: Int(fps.rounded()),
    ] as [String: Any],
])
input.expectsMediaDataInRealTime = false
writer.add(input)

reader.startReading()
writer.startWriting()
writer.startSession(atSourceTime: .zero)
let q = DispatchQueue(label: "enc")
input.requestMediaDataWhenReady(on: q) {
    while input.isReadyForMoreMediaData {
        if let buf = out.copyNextSampleBuffer() { input.append(buf) }
        else { input.markAsFinished(); writer.finishWriting { sema.signal() }; return }
    }
}
sema.wait()
print(writer.status == .completed ? "ok" : "failed: \(String(describing: writer.error))")
