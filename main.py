from camera import test_and_detect, capture_training_images
from modelTraining import train_model
from recognizer import recognize_attendence

capture_training_images("Ansary")
capture_training_images("AnsaryMask", 0, "Training Mask Images")
train_model()
recognize_attendence()
