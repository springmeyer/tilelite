# TileLite

A lightweight, multi-process, tile-server using Mapnik.

A gateway tool to [TileStache](http://tilestache.org/) or [TileCache](http://tilecache.org).

## Status

- Written originally in 2009/2010 and versioned at https://bitbucket.org/springmeyer/tilelite
- Moved from https://bitbucket.org/springmeyer/tilelite to github in 2013
- Not currently developed or maintained.

## Depends

 - Python 2.x
 - Mapnik (>= 2.x) and a Mapnik xml mapfile you wish to serve.

## Installing

    git clone https://github.com/springmeyer/tilelite.git
    cd tilelite
    sudo python setup.py install

## Usage
    
    liteserv.py <xml> [options]

 - Can be deployed with `apache` + `mod_wsgi` using one thread and many processes.
 - Able to read from an optional configuration file for customization of various rendering and caching parameters.

## Configuration

See the notes in the 'docs' folder and the sample 'tilelite.cfg' in the 'utils' folder.
