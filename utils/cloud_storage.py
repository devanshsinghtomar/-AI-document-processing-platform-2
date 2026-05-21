import cloudinary

import cloudinary.uploader


cloudinary.config(

    cloud_name="dm2itd8tx",

    api_key="178668573783122",

    api_secret="@dm2itd8tx"
)


def upload_to_cloud(file_path):

    response = cloudinary.uploader.upload(
        file_path
    )

    return response["secure_url"]
