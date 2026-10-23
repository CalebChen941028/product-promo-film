// Text and its boxes in a picture, with the system's own text recognition (macOS Vision). No download, no network.
// swiftc -O scripts/ocr.swift -o <cache>/pf-ocr ; pf-ocr <image>  → JSON [{"text": "…", "rect": [x, y, w, h]}] in image pixels
import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count > 1, let img = NSImage(contentsOfFile: args[1]),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("[]"); exit(0) }
let W = Double(cg.width), H = Double(cg.height)
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
req.recognitionLanguages = ["zh-Hans", "zh-Hant", "en-US", "ja-JP"]
try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
var out: [[String: Any]] = []
for o in req.results ?? [] {
  guard let t = o.topCandidates(1).first?.string else { continue }
  let b = o.boundingBox   // normalised, origin bottom-left
  out.append(["text": t, "rect": [Int(b.minX * W), Int((1 - b.maxY) * H), Int(b.width * W), Int(b.height * H)]])
}
let data = try! JSONSerialization.data(withJSONObject: out)
print(String(data: data, encoding: .utf8)!)
