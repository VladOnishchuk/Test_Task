## Setup 

1. Clone the repository:
    ```sh
    $ git clone git@github.com:VladOnishchuk/TestTask.git
    ```
2. Populate env.example file and rename it on .env
3. Build container by command:
    ```sh
    $ docker bild -t assistant_app .
    ```
4. Run container by command
    ```sh
    $ docker run -d --name myapp -p 8000:8000 assistant_app
    ```
   

## App
By url http://0.0.0.0:8000/docs/ there is swagger doc, generated automatically by FastAIP.


