# textualize
Convert audio to text with Google speech-to-text Api.  
you can only upload `mp3/wav` file type and is within 200MB, and it can transcribe audio files to only `English/Japanese`.

you can find sample audio files are under `resources` directory.

## Libraries

|Function|Version|Description|
----|----|----
|Python|3.96|Programing Language|
|Streamlit|0.86.0|Framework|
|google-cloud-speech|2.7.0|Speech Recognition API
|juypyter core|4.7.1|Jupyter core library|
|juypyter lab|3.1.6|Interactive dev environment library
|janome|0.4.1|morphological analysis library|
|Docker|20.10.8|Container virtualization tools

## Project Structure
```
Textualize
  ┣ resources          ← You can find sample audio files. (English/Japanese)
  ┣ src
  ┃  ┣ app.py
  ┃  ┣ language.py
  ┃  ┗ config
  ┃     ┗ secret.json  ← You need to create this file.
  ┃
  ┣ .gitignore
  ┣ docker-compose.yml
  ┣ Dockerfile
  ┗ README.md
```

## How to Set-up
### Summary
you can skip these 1 ~ 3 process this time.
1. Login to GCP and create IAM user for this project. 
2. Download from authentication info in GCP to call speech-to-text API. (`secret.json`)
3. Rename the downloaded file to `secret.json` and put it under `config` directory.


4. Run Docker-compose up
5. Access to `localhost:8501`

### Details
1. clone the source code.
```
git clone git@github.com:shxn0/textualize.git
```

2. create `secret.json` file under `config` directory.  
here is a sample template for secret.json.

```
{
  "type": "",
  "project_id": "textualize",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}

```

3. confirm you are in textualize root project.
```
~/$PATH/textualize
```

4. run a command as below. run docker via daemon in background.  
installing necessary libraries automatically when you run docker-compose up.
```
docker-compose up -d --build
```

5. open your browser and access to `localhost:8501`. (streamlit uses `:8501` port)  
If this screen shows up, you are success to run web app.

![top-page](https://user-images.githubusercontent.com/30136112/129522482-9f384435-d116-49e2-8768-d616e1415b17.png)


### How to Use
1. you can find sample audio files are under `resources` directory.
2. upload audio file. you can upload only mp3/wav file type and is within 200MB.
3. press `Start` to transcribe audio to text.
4. you can search three words in transcribed text.
5. you can see 5 words before and after the searched word in a table.

ex.
![search-function](https://user-images.githubusercontent.com/30136112/129526363-3bef1fcb-eaf8-477e-a399-60891f4ecce2.png)



