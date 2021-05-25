from camera import test_and_detect, capture_training_images
from modelTraining import train_model
from recognizer import recognize_attendence

print(capture_training_images("Ansary"))
train_model()
recognize_attendence()
