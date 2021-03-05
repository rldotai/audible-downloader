# Description

Some miscellaneous notes that might be useful for myself or others looking to hack on this project.  

# Running a Selenium Chrome Instance via Docker

Starting a `selenium` compatible Chrome instance in Docker.

```bash
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-beta-1-20210215
```

In another shell, use Selenium's remote webdriver:

```python
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
```

# Missing `mp4v2` AKA `mp4v2-utils`

`AAXtoMP3` will complain about not having access to `mp4chaps` and `mp4art`, suggesting I install the `mp4v2-utils` package; however, Ubuntu 20.04 doesn't have that package available, apparently because the upstream is unmaintained.


I am not sure how beneficial these things are, since everything seems to work when I'm playing the files with `mpv` and given that I'm splitting the files on a per-chapter basis anyways.

However, others have found a workaround by installing using:

```bash
wget http://archive.ubuntu.com/ubuntu/pool/universe/m/mp4v2/libmp4v2-2_2.0.0~dfsg0-6_amd64.deb && \
wget http://archive.ubuntu.com/ubuntu/pool/universe/m/mp4v2/mp4v2-utils_2.0.0~dfsg0-6_amd64.deb && \
dpkg -i libmp4v2-2_2.0.0~dfsg0-6_amd64.deb && \
dpkg -i mp4v2-utils_2.0.0~dfsg0-6_amd64.deb && \
rm *.deb
```

I'm not terribly stoked about downloading unmaintained software compiled for a different version of my OS, but the above snippet could be used in a `Dockerfile` if I find this necessary in the future.