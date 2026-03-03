#install in the taminal or the cmd : > pip install qrcode 
import qrcode
import sys 

# Create a QR code object
qr = qrcode.QRCode(
    version=1,# set the qr code version (size and complexity).Adjust as needed.
    error_correction=qrcode.constants.ERROR_CORRECT_L,# Set the error corection 
    box_size=10,# seting the size of each black model in pixels(affects image size)
    border=4,# setting the width of the white border around the qr code (in modules )
)

# Add data to the QR code
qr.add_data("https://classroom.google.com/")

# Generate the QR code image
qr.make(fit=True)

# Create an image from the QR code
img = qr.make_image(fill_color="black", back_color="white")

#save image location 
esired_location = "QR codes"

# Save the image
img.save("myqrcode.png")