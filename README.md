
# Audible Downloader


- Uses [`audible-activator`](https://github.com/inAudible-NG/audible-activator) to get the authentication for the streams.
	- I modified the file a little bit to add support for the `remote` WebDriver.
- To do this without having to mess around configuring Chrome/Python/selenium, it uses [`docker-selenium`](https://github.com/SeleniumHQ/docker-selenium) to create standalone containers that can be controlled remotely.
- Converts AAX files to MP3 using [`AAXtoMP3`](https://github.com/KrumpetPirate/AAXtoMP3).


If I get around to it, I would like to try doing all of the above using containers, but presently I am just using containers to avoid having to futz with setting up Selenium/WebDriver stuff with my usual browser.

# Setup

Clone this repository, ensuring submodules are cloned as well:

```bash
git clone https://github.com/rldotai/audible-downloader.git --recurse-submodules 
```

I'm assuming you have `docker` installed; if not, you should probably do that.

*This is what worked for me, running Ubuntu 20.04; if you're running a different OS or something's not working, you may have to make some modifications of your own. Check the READMEs in the submodules for guidance on how to do that.*

## Audible Activator

Install the requirements and copy `modified-audible-activator.py` to add the "remote" option. 

```bash
pip install -r requirements.txt
cp modified-audible-activator.py audible-activator/modified-audible-activator.py
```

## AAXtoMP3

Install prerequisites:

```bash
sudo apt-get install ffmpeg x264 x265 bc mediainfo
```

# Usage

## Get Activation Code 

### Using Selenium Docker Image

This avoids the need to setup a WebDriver-capable browser directly on your machine, because we instead download and run a container that's running a compatible version of Chrome.
If you already have Selenium setup and working on your host, you might be better off just running it directly (rather than by using a container) -- see `audible-activator` on how to do that.
Alternatively, you could perhaps find the activation bits by just using your browser's DevTools, if neither approach seems appealing.

Without further ado:


```bash
# Start the Chrome WebDriver container
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-beta-1-20210215

# Get the activation bytes
python audible-activator/modified-audible-activator.py --remote --username=<USERNAME> --password=<PASSWORD>
```

This should print your activation/auth code in the terminal. 


## Convert the Files

Supposing that my authcode was `1337c0d3` and that my audiobooks were stored in `~/Downloads/audiobooks` as a bunch of `.aax` files, I could convert them to `m4a` and store the results in `output` using:

```bash
# Convert the books
python convert-books.py --authcode=1337c0d3 --outdir=output ~/Downloads/audiobooks/*.aax
```

Further details can be found via `python convert-books.py --help`.

Note that some of the options (like the filename formats and output filetype) are hardcoded, largely because I am lazy and increasingly keen on finishing up this script so I can listen to some audiobooks.
