# Image Compress - Python (Learning Project)

This project aims to create a simple solution for compressing images using the Pillow library.  

The project has a web server created with Flask, providing a self-hosted base solution for image optimization via API.


## How to Use

You can use the **online** or **offline** version. For PC packages, prefer the offline version. If your purpose is to run this within software or a plugin, use the API.

You can use the free server `https://imgc1.col-pro.net/compress` or host it yourself.

For Windows users, download the releases and run.
## Install API in Docker

On your PC, create a folder and put the files `Dockerfile`, `img-compress.py`, `requirements.txt`.  

Build the Docker image with:

```bash
docker build -t imgcompress .
```   
Run the image with: 
```bash
docker run --restart always -p 5000:5000 --name imgcompress imgcompress
```   

Press ```Ctrl+C``` for stop and run 
```bash 
docker start imgcompress
``` 
for start the script.

Note: If you're not using Docker, you can use ```screen``` with the following steps:
Type ```screen```, ```pip install -r requirements.txt```, ```python3 img-compress.py```, ```Ctrl+A```, then press ```D```.
## How to use API

#### cURL command with a local file (example with local file and Fat quality):

```cURL
curl --location 'http://localhost:5000/compress?quality=Fat' \
--form 'file=@"/path/to/your/image.jpg"'

```

| Parameter   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `quality` | `string` | Light/Medium/High/Fat |

#### cURL command for image in base64:

```cURL
curl --location 'http://localhost:5000/compress?quality=Fat' \ 
--header 'Content-Type: application/json' \ 
--data '{"image":"iVBORw0KGgoAAAANSUhEUgAAAvUAAAKWCAYAAADJImZ5AAAAAXNSR0IArs4c6QAAAAR..."}'

```

| Parameter   | Typo       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `quality` | `string` | Light/Medium/High/Fat |


## Remember

This project is made for learning about Python, requests, Pillow, and tkinter... for now.