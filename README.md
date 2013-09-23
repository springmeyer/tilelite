## TileLite

A lightweight, multi-process, tile-server written as a WSGI app.

A 'gateway' tool to [TileStache](http://tilestache.org/) or [TileCache](http://tilecache.org).

### Requires
 * Python
 * Mapnik (>= 2.x) and a Mapnik xml or mml mapfile you wish to serve.

### Installing

    git clone https://github.com/springmeyer/TileLite.git
    cd TileLite
    sudo python setup.py install

### Usage
    
    liteserv.py <xml> [options]

 * Can be deployed with Mod_wsgi using one thread and many processes.
 * Able to read from an optional configuration file for customization of various rendering and caching parameters.

## Configuration

See the notes in the 'docs' folder and the sample 'tilelite.cfg' in the 'utils' folder.