# mock-cameras

Mock the cameras gateway, by publishing the images of a dataset on the *is* architecture.

The video files must be on the following format at folder:
```txt
p001g01c00.mp4
p001g01c01.mp4
p001g01c02.mp4
...
```
And so on, for *n* number of cameras. You can see the images published on the topic:
```
"CameraFrame.<camera_id>.Frame"
```

### Developing 

You can use a docker container to run this application. First, build the image:

```bash
git clone https://github.com/luizcarloscf/mock-cameras.git
cd mock-cameras
docker build -f etc/docker/Dockerfile --tag=mockcameras .
```

And run the container. Remember to pass the bind to the directory of the video files, the directory of the project and update the correct [*options.json*](https://github.com/luizcarloscf/mock-cameras/blob/master/etc/conf/options.json) file

```bash
docker run -it -v <path_to_video_files>:/datasets -v $(pwd):/project mockcameras python3 src/service.py
```
**Or** if you wanna, you can run the [*bootstrap.sh*](https://github.com/luizcarloscf/mock-cameras/blob/master/bootstrap.sh) in your own computer. It will work for Ubuntu 18.04 only.
```bash
git clone https://github.com/luizcarloscf/mock-cameras.git
./bootstrap.sh
python3 src/service.py
```