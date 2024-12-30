import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model/weights/best.pt')


def get_detected_tag(image):
    results = model(image)

    detected_tags = results.names

    boxes = results.xywh[0][:, :-1].tolist()

    areas = [box[2] * box[3] for box in boxes]
    max_area_index = areas.index(max(areas))
    largest_bbox_class = results.xywh[0][max_area_index, -1].item()
    largest_bbox_tag = detected_tags[int(largest_bbox_class)]

    return largest_bbox_tag or None

