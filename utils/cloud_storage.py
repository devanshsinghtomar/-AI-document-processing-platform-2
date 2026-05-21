import cloudinary

import cloudinary.uploader


cloudinary.config(

    cloud_name="YOUR_CLOUD_NAME",

    api_key="YOUR_API_KEY",

    api_secret="YOUR_API_SECRET"
)


def upload_to_cloud(file_path):

    response = cloudinary.uploader.upload(
        file_path
    )

    return response["secure_url"]