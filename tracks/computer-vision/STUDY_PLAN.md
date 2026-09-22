# Six weeks of Computer Vision

Roughly 6–8 hours a week. Weighted toward detection, architectures and training, because
that is where applied vision work concentrates.

There is no exam at the end of this. The target is competence you can use, and the
assessments exist to tell you whether you have it.

Every week ends with the same loop:

```bash
./sim.py -k computer-vision practice -d <topic>   # learn
./sim.py review                                   # whatever is due
./sim.py stats                                    # where you actually stand
```

And every day you study at all:

```bash
./sim.py review    # due questions
./sim.py flash     # due flashcards
```

---

## Week 0 — baseline (1 hour)

```bash
./sim.py -k computer-vision exam
```

Take it cold. Note the per-topic numbers; you will compare in week 6.

Before anything else, read one cheat sheet:

```bash
./sim.py -k computer-vision cheat -d pipeline-traps
```

Nine traps, each of which has silently broken a production pipeline. They cost more hours in
practice than any modelling decision, and they recur in every week that follows.

---

## Week 1 — Images and geometry (16% of the track)

*Topic areas: Image Fundamentals (8%), Classical Vision and Geometry (8%)*

**Read** — [OpenCV tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html):
filtering, morphology, geometric transforms, features, calibration.

**Build** — load an image with `cv2.imread`, display it with matplotlib without converting,
and look at the result. Then fix it. Do the same with `cv2.add` versus `+` on a bright
region. Two minutes each, and neither bug will ever cost you an afternoon again.

**Know cold**
- BGR vs RGB, and that nothing errors — accuracy just drops.
- Median for salt-and-pepper, Gaussian for general smoothing (separable, so two 1D passes),
  bilateral when edges must survive.
- Opening = erode then dilate (removes specks). Closing is the reverse (fills holes).
- `INTER_AREA` to shrink, linear or cubic to enlarge, **nearest** for label masks.
- Affine: 6 DOF, 3 point pairs, parallel lines preserved. Homography: 8 DOF, 4 pairs.
- A homography is valid only for a plane or a purely rotating camera. Parallax breaks it —
  low inlier counts are the symptom.
- Depth = focal length × baseline ÷ disparity.

```bash
./sim.py -k computer-vision practice -d image-fundamentals
./sim.py -k computer-vision practice -d classical-cv
```

---

## Week 2 — Architectures and training (24%)

*Topic areas: Convolutional Architectures (12%), Training Vision Models (12%)*

The heaviest week. Two topic areas that everything later depends on.

**Read**
- [CS231n notes](https://cs231n.github.io/) — still the best free written treatment
- [ResNet](https://arxiv.org/abs/1512.03385) · [MobileNet](https://arxiv.org/abs/1704.04861)

**Build** — fine-tune a torchvision backbone on a small dataset twice: once with the
backbone frozen, once fully unfrozen at the same learning rate. Watch the second one destroy
the pretrained features. That is catastrophic forgetting, and seeing it once is worth more
than reading about it.

**Know cold**
- Weight sharing → few parameters and translation equivariance. Not rotation invariance.
- Receptive field compounds with depth. Two 3×3 beats one 5×5: same field, fewer parameters,
  extra non-linearity.
- BatchNorm uses batch statistics in training and running statistics at inference — which is
  why `model.eval()` matters. GroupNorm when batches are tiny.
- Residual connections are what make depth trainable at all.
- Augmentation should simulate variation you will actually meet. Vertical flip is wrong for
  street scenes and fine for satellite imagery.
- Mixed precision needs a loss scaler: small FP16 gradients underflow to zero.
- Sawtooth GPU utilisation means the *data pipeline* is starving the GPU, not that the model
  is slow.

```bash
./sim.py -k computer-vision practice -d cnn-architectures
./sim.py -k computer-vision practice -d training-vision
```

---

## Week 3 — Detection (14%)

*The single heaviest topic area. Give it a full week.*

**Read** — [YOLO](https://arxiv.org/abs/1506.02640) ·
[Focal loss](https://arxiv.org/abs/1708.02002) ·
[FPN](https://arxiv.org/abs/1612.03144) ·
[COCO evaluation](https://cocodataset.org/#detection-eval)

**Build** — train a small detector on a few hundred images, then sweep the confidence
threshold and plot precision against recall. Pick an operating point for a stated purpose.
Most people never do this and deploy whatever the default was.

**Know cold**
- One-stage vs two-stage. Anchors as priors; anchor-free heads regress geometry directly.
- IoU appears in three different places — anchor assignment, NMS, evaluation — with
  different thresholds meaning different things.
- COCO mAP averages IoU 0.5:0.95 and is systematically lower than VOC mAP at 0.5. Never
  compare the two numbers.
- mAP averages over all thresholds, so it says nothing about the operating point you deploy.
- Small objects missed → resolution and which pyramid level owns small scales.
- Boxes consistently offset → letterbox padding not undone.
- Crowded objects deleted → NMS too aggressive; try Soft-NMS.

```bash
./sim.py -k computer-vision practice -d detection
```

---

## Week 4 — Segmentation and transformers (21%)

*Topic areas: Segmentation (11%), Vision Transformers and Multimodal (10%)*

**Read**
- [U-Net](https://arxiv.org/abs/1505.04597) · [Mask R-CNN](https://arxiv.org/abs/1703.06870)
- [ViT](https://arxiv.org/abs/2010.11929) · [CLIP](https://arxiv.org/abs/2103.00020)

**Know cold**
- Semantic cannot count — two touching cars are one blob. Instance and panoptic can.
- U-Net skips carry high-resolution detail the bottleneck destroyed. Without them, boundaries
  blur.
- Checkerboard artefacts = transposed conv with stride not dividing kernel size. Use
  resize-then-convolve.
- Dice stays sensitive when foreground is tiny; cross-entropy alone gets swamped.
- 97% pixel accuracy with 0.41 mIoU means large classes dominate. Read the per-class table.
- Dice = 2·IoU/(1+IoU) — same ranking, different numbers. Check which a paper reports.
- ViTs need more data than CNNs because they must *learn* locality and translation
  equivariance rather than getting them free.
- Attention cost scales with the square of tokens, and tokens with the square of resolution —
  resolution enters at the fourth power.

```bash
./sim.py -k computer-vision practice -d segmentation
./sim.py -k computer-vision practice -d vision-transformers
```

---

## Week 5 — Video, data and deployment (25%)

*Topic areas: Video and Tracking (8%), Data and Evaluation (9%), Deployment and Edge (8%)*

The week that separates a model from a system.

**Read**
- [SORT](https://arxiv.org/abs/1602.00763) · [DeepSORT](https://arxiv.org/abs/1703.07402)
- [TensorRT docs](https://docs.nvidia.com/deeplearning/tensorrt/) ·
  [ONNX export](https://pytorch.org/docs/stable/onnx.html)

**Build** — export a trained model to ONNX, run it through both PyTorch and ONNX Runtime on
the same fixed inputs, and diff the outputs. Then do it again at a different input size.
Dynamic axes stop being theoretical.

**Know cold**
- Detect periodically and track between — frames are highly redundant.
- Association is a bipartite assignment; Kalman predicts, appearance re-ID survives crossings.
- MOTA under-penalises identity switches; IDF1 exposes them. Report both.
- Inter-annotator agreement is a **ceiling** on measured performance.
- Group splits by video, patient or site. Random splits leak near-duplicates.
- ROC flatters imbalanced problems; use precision-recall.
- INT8 needs calibration data; FP16 does not. INT8 often preserves classification accuracy
  while hurting detection mAP, because coordinates feed straight into IoU.
- A TensorRT engine is tied to its GPU architecture. Rebuild per target.
- Latency vs throughput: batching raises one and raises the other too.
- Notebook-accurate, production-poor, identical weights → preprocessing parity.

```bash
./sim.py -k computer-vision practice -d video-tracking
./sim.py -k computer-vision practice -d data-evaluation
./sim.py -k computer-vision practice -d deployment-edge
./sim.py -k computer-vision exam      # compare against week 0
```

---

## Week 6 — Consolidation

Stop reading new material. Two or three full timed assessments, review between them, and read
the cheat sheet for anything still under 80%.

```bash
./sim.py -k computer-vision exam
./sim.py review
./sim.py flash -d pipeline-traps
./sim.py stats
./sim.py cheat -d <weakest area>
```

You are done when `./sim.py stats` shows weighted accuracy above 85% with every topic area
attempted and no concept below target in an 11–14% area.

---

## There is no certificate at the end of this

That is deliberate, and worth saying plainly. No vendor certifies applied computer vision:
the adjacent credentials are multimodal generative AI (NVIDIA NCA-GENM), a cloud platform
exam where vision is 15–20% of the content (Microsoft AI-102), or course-completion badges
(OpenCV University). None of them is a computer vision exam.

So the evidence you finish with is not a badge. Build something: a detector on your own
images, exported, quantised and measured end to end. That demonstrates more than any of the
three credentials above, and this track is preparation for doing it.
