# thomasjpfan.com

Repo for personal [blog](https://thomasjpfan.com).

## Build docker builder

The `builder` directory builds a docker image that builds this site. To build the builder run:

```bash
make builder
```

## Local Development

Start up a shell:

```bash
 docker run --rm --name stuff -p 8000:8000 -v $PWD:/blog -ti thomasjpfan/pelican-blog-builder /bin/sh
```

And run `make devserver` and to stop `make stopserver`.

## Deploy Using Rsync

1. Have the following defined in env or an `.envrc`:

```bash
export SSH_HOST=[***]
export SSH_PORT=[***]
export SSH_USER=[***]
export SSH_TARGET_DIR=[***]
```

1. Using the builder to build site:

```bash
make build_site
```

1. Deploy

```bash
make rsync_only
```
