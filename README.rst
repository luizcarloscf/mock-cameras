============
Mock Cameras
============

Mock the cameras gateway, by publishing the images of a dataset on the *is* architecture.

About
-----

The dataset contains video files that identify the person, the gesture and the camera.

    .. code:: bash
    
        .
        ├── p001g01c00.mp4
        ├── p001g01c01.mp4
        ├── p001g01c02.mp4
        ├── p001g01c03.mp4
        ├── p001g02c00.mp4
        ├── p001g02c01.mp4
        ├── p001g02c02.mp4
        └── ..




Options
-------
    .. code:: json

        {
            "broker_uri": "amqp://rabbitmq.default",
            "zipkin_uri": "http://zipkin.default:9411",
            "folder": "/datasets",
            "fps": 9,
            "cameras_id": [
                0,
                1,
                2,
                3
            ],
            "videos": [
                {
                    "person_id": 1,
                    "gesture_id": 1,
                    "iterations": 1
                }
            ],
            "loop": true
        }

Kubernetes
----------

The dataset is mounted on every machine of the Kubernetes Cluster, because of the storage server. See `etc/k8s/deployment.yaml <https://github.com/luizcarloscf/mock-cameras/blob/master/etc/k8s/deployment.yaml>`__ for more info. To apply,

    .. code:: bash

        $ git clone https://github.com/luizcarloscf/mock-cameras.git
        $ cd mock-cameras
        $ kubectl apply -f etc/k8s/deployment.yaml


Developing
----------

You can build the docker image on your local machine to run this application. Remember to pass the correct ENV variables on **Makefile**.

    .. code:: bash

        $ git clone https://github.com/luizcarloscf/mock-cameras.git
        $ cd mock-cameras
        $ make VERSION="0.0.1" USER="<docker_user>" build


And run the container. Remember to pass the bind to the directory of the video files and update the correct `options.json <https://github.com/luizcarloscf/mock-cameras/blob/master/etc/conf/options.json)>`__ file


**Or** if you wanna, you can run the `bootstrap.sh <https://github.com/luizcarloscf/mock-cameras/blob/master/bootstrap.sh>`__ in your own computer. It will work for Ubuntu 18.04 only.

    .. code:: bash

        $ git clone https://github.com/luizcarloscf/mock-cameras.git
        $ cd mock-cameras
        $ make install
        $ python3 src/service.py
