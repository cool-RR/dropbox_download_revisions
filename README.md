# dropbox_download_revisions.py

Script to download all revisions of a Dropbox file

Usage:

    ./dropbox_download_revisions.py my_file.txt
    
You'll be asked for a Dropbox API key, you can get one [here](https://dropbox.github.io/dropbox-api-v2-explorer/#auth_token/from_oauth1) . Just press on "Get Token".

You can pass `--save-api-key` to have it saved for next time.

Requires:

  * Python 3.6+
  * `pip install click dropbox`
  
Copyright [Ram Rachum](https://ram.rachum.com), MIT License