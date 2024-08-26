import qrcode
import io

def qr_generator(data):
    # Create a QR Instance
    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  
        border=4, 
    )
    
    # Add data to QR
    qr.add_data(data)
    qr.make(fit=True)

    # Create the QR image
    imagen = qr.make_image(fill="black", back_color="white")

    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    imagen.save(img_byte_arr)
    img_byte_arr = img_byte_arr.getvalue()
    
    # Return bytes
    return img_byte_arr


# Usage example
if __name__ == "__main__":
    var = '\n[Interface]\nPrivateKey = 0GA9VzLgUB4F6i7pXLb4HR71BjdIbs2pnTwvigPb5Eo=\nAddress = 10.8.0.3/24\nDNS = 1.1.1.1\n\n[Peer]\nPublicKey = N9QHWlcwrDrG7FQrqBtrF/oymeG3NbltcM6xLSX3zFE=\nPresharedKey = VLZqyTYtRxmKJn4PleROXLpyylKp86vw6dnCQVieXQ0=\nAllowedIPs = 0.0.0.0/0, ::/0\nPersistentKeepalive = 0\nEndpoint = 83.55.112.78:51820'
    #qr_generator(var, Test=True)
    print(qr_generator(var))

'''
import qrcode
from PIL import Image

def qr_logo_generator(data, file_name="qr_code.png", logo_path="wireguard_logo.png"):
    # Create a QR Instance
    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=10,
        border=4,
    )
    
    # Add data to QR
    qr.add_data(data)
    qr.make(fit=True)

    # Create the QR image
    qr_img = qr.make_image(fill="black", back_color="white").convert('RGB')
    
    # Open WireGuard logo
    logo = Image.open(logo_path)

    # Resize logo
    logo_size = int(qr_img.size[0] / 5)
    logo = logo.resize((logo_size, logo_size))

    # Center logo
    pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)

    # Paste centered logo
    qr_img.paste(logo, pos, logo)

    # Save final image
    qr_img.save(file_name)
    print(f"QR save in: {file_name}")

# Usage example
configuracion_wireguard = """
[Interface]
PrivateKey = PRIVATE_KEY
Address = 10.0.0.1/24
DNS = 8.8.8.8

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = dominio_o_ip:51820
AllowedIPs = 0.0.0.0/0, ::/0
"""
qr_logo_generator(configuracion_wireguard, "wireguard_qr.png", "wireguard_logo.png")
'''
