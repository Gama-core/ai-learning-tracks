# Free study material for Applied Computer Vision

This track is vendor-neutral, so the reading is too. Everything here is free. Tagged by the
topic area it supports:

`IF` image fundamentals · `CV` classical geometry · `CN` CNN architectures · `TV` training
`DE` detection · `SG` segmentation · `VT` vision transformers · `VD` video & tracking
`EV` data & evaluation · `DP` deployment & edge

---

## Libraries and documentation

| Resource | Areas |
|---|---|
| [OpenCV tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — filtering, morphology, transforms, features, calibration, flow | IF CV VD |
| [OpenCV camera calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) | CV |
| [torchvision models and transforms](https://pytorch.org/vision/stable/index.html) | CN TV |
| [PyTorch data loading](https://pytorch.org/docs/stable/data.html) | TV |
| [PyTorch AMP (mixed precision)](https://pytorch.org/docs/stable/amp.html) | TV |
| [PyTorch reproducibility notes](https://pytorch.org/docs/stable/notes/randomness.html) | EV |
| [Albumentations](https://albumentations.ai/docs/) — augmentation that transforms boxes and masks with the image | TV SG |
| [Ultralytics docs](https://docs.ultralytics.com/) — practical detection training and inference | DE |
| [ONNX](https://onnx.ai/) and [PyTorch ONNX export](https://pytorch.org/docs/stable/onnx.html) | DP |
| [TensorRT documentation](https://docs.nvidia.com/deeplearning/tensorrt/) | DP |
| [DeepStream SDK](https://developer.nvidia.com/deepstream-sdk) — multi-camera streaming pipelines | VD DP |
| [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) | EV |
| [COCO evaluation definition](https://cocodataset.org/#detection-eval) — what mAP actually computes | DE EV |

## Free courses

- **OpenCV free course** — <https://opencv.org/university/free-opencv-course/> · three hours of
  practical image and video manipulation, with an official certificate.
- **OpenCV University free courses** — <https://opencv.org/university/free-courses/>
- **Stanford CS231n materials** — <https://cs231n.github.io/> · the notes remain the best free
  written treatment of CNNs, training dynamics and architectures.
- **Hugging Face Computer Vision Course** — <https://huggingface.co/learn/computer-vision-course>
- **Fast.ai Practical Deep Learning** — <https://course.fast.ai/> · strong on the training and
  transfer-learning craft this track emphasises.
- **Kaggle Computer Vision** — <https://www.kaggle.com/learn/computer-vision>

## Papers, by topic area

**Architectures (`CN`)**
- VGG — <https://arxiv.org/abs/1409.1556>
- ResNet — <https://arxiv.org/abs/1512.03385>
- Network in Network (1x1 convolutions, GAP) — <https://arxiv.org/abs/1312.4400>
- MobileNet (depthwise separable) — <https://arxiv.org/abs/1704.04861>
- EfficientNet (compound scaling) — <https://arxiv.org/abs/1905.11946>
- Dilated convolutions — <https://arxiv.org/abs/1511.07122>
- Group Normalization — <https://arxiv.org/abs/1803.08494>
- Visualizing and understanding CNNs — <https://arxiv.org/abs/1311.2901>
- How transferable are features? — <https://arxiv.org/abs/1411.1792>

**Detection (`DE`)**
- Faster R-CNN — <https://arxiv.org/abs/1506.01497>
- YOLO — <https://arxiv.org/abs/1506.02640> · YOLO9000 — <https://arxiv.org/abs/1612.08242>
- Focal loss / RetinaNet — <https://arxiv.org/abs/1708.02002>
- Feature Pyramid Networks — <https://arxiv.org/abs/1612.03144>
- FCOS (anchor-free) — <https://arxiv.org/abs/1904.01355>
- DETR — <https://arxiv.org/abs/2005.12872>
- Soft-NMS — <https://arxiv.org/abs/1704.04503>
- GIoU loss — <https://arxiv.org/abs/1902.09630>
- YOLOv4 (mosaic, bag of freebies) — <https://arxiv.org/abs/2004.10934>

**Segmentation (`SG`)**
- U-Net — <https://arxiv.org/abs/1505.04597>
- Fully Convolutional Networks — <https://arxiv.org/abs/1411.4038>
- Mask R-CNN (RoIAlign) — <https://arxiv.org/abs/1703.06870>
- DeepLabv3 (ASPP) — <https://arxiv.org/abs/1706.05587>
- V-Net (Dice loss) — <https://arxiv.org/abs/1606.04797>
- Panoptic segmentation — <https://arxiv.org/abs/1801.00868>
- Segment Anything — <https://arxiv.org/abs/2304.02643>
- Deconvolution and checkerboard artifacts — <https://distill.pub/2016/deconv-checkerboard/>

**Transformers and multimodal (`VT`)**
- Vision Transformer — <https://arxiv.org/abs/2010.11929>
- Swin Transformer — <https://arxiv.org/abs/2103.14030>
- CLIP — <https://arxiv.org/abs/2103.00020>
- DINO — <https://arxiv.org/abs/2104.14294>
- Masked Autoencoders — <https://arxiv.org/abs/2111.06377>
- Latent diffusion — <https://arxiv.org/abs/2112.10752>
- Classifier-free guidance — <https://arxiv.org/abs/2207.12598>

**Video and tracking (`VD`)**
- SORT — <https://arxiv.org/abs/1602.00763>
- DeepSORT — <https://arxiv.org/abs/1703.07402>
- MOT16 benchmark — <https://arxiv.org/abs/1603.00831>
- IDF1 metric — <https://arxiv.org/abs/1609.01775>
- Two-stream networks — <https://arxiv.org/abs/1406.2199>
- I3D / Kinetics — <https://arxiv.org/abs/1705.07750>

**Training and deployment (`TV` `DP`)**
- Mixup — <https://arxiv.org/abs/1710.09412>
- Label smoothing (Inception-v3) — <https://arxiv.org/abs/1512.00567>
- Large-batch training and warmup — <https://arxiv.org/abs/1706.02677>
- Knowledge distillation — <https://arxiv.org/abs/1503.02531>
- Pruning filters for efficient ConvNets — <https://arxiv.org/abs/1608.08710>
- Rethinking ImageNet pre-training — <https://arxiv.org/abs/1902.07208>
- On translation invariance in CNNs — <https://arxiv.org/abs/2010.02178>

## A note on what this track is

This is a **Gama Core learning track, not a certification**. No vendor exam, credential or
cut score exists for this material — that absence is precisely why the track was built. The
topic weights are our editorial judgement of where applied computer vision work
concentrates, not a published blueprint, and should be read as a claim rather than a
citation.

If you want a credential adjacent to this material, the honest options are NVIDIA's
[NCA-GENM](https://www.nvidia.com/en-us/learn/certification/generative-ai-multimodal-associate/)
(multimodal generative AI, only partly vision), Microsoft's
[AI-102](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/)
(Azure AI Engineer, roughly a fifth vision), or [OpenCV University's](https://opencv.org/university/)
course certificates.
