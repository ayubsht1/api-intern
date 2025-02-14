import base64

def base_encoder(data:str):
    return base64.b64encode(data.encode()).decode()


def base_decoder(data):
    return base64.b64decode(data).decode()