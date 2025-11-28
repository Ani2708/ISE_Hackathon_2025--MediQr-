import qrcode

# The URL your QR should lead to
url = "http://10.117.205.107:5000/patient?id=PATIENT-8349922"

# Generate QR code
qr = qrcode.make(url)

# Save as an image
qr.save("patientQRCode.png")

print("QR code generated successfully!")
