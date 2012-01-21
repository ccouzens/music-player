#!/usr/bin/env python
import gi
from gi.repository import Tracker, GObject, Gtk, GdkPixbuf
import os.path
import md5
import unicodedata
from xdg.BaseDirectory import xdg_cache_home

album_query = """
SELECT ?title ?artist_name
WHERE {
  ?album a nmm:MusicAlbum; 
      nmm:albumTitle ?title ;
      nmm:albumArtist [ nmm:artistName ?artist_name ] .
  ?song nmm:musicAlbum ?album .
}  
GROUP BY ?album
"""

if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file("window.glade")
    window = builder.get_object("window1")
    album_store = builder.get_object("album-store")
    window.show_all()
    window.connect("destroy", Gtk.main_quit)

    media_art_directory = os.path.join(xdg_cache_home, 'media-art', '90')

    conn = Tracker.SparqlConnection.get (None)
    cursor = conn.query(album_query, None)
    while cursor.next (None):
        md5_string = md5.new(
            cursor.get_string(1)[0] + "\t" + cursor.get_string(0)[0]
        ).hexdigest()

        album_art_pixbuf = None
        album_art_filename = os.path.join(media_art_directory, 'album-' + md5_string + '.jpg')

        try:
            album_art_pixbuf = GdkPixbuf.Pixbuf.new_from_file(album_art_filename)
        except Exception as e:
            print e
            album_art_pixbuf = None

        album_store.append((cursor.get_string(0)[0],album_art_pixbuf))
        print unicode(cursor.get_string(1)[0], "utf-8"), cursor.get_string(0)[0]

    Gtk.main()
