#!/usr/bin/env python
import gi
from gi.repository import Tracker, GObject, Gtk
import md5
import unicodedata

album_query = """
SELECT ?title ?artist_name
WHERE {
  ?album a nmm:MusicAlbum; 
      nmm:albumTitle ?title ;
      nmm:albumArtist [ nmm:artistName ?artist_name ] .
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


    conn = Tracker.SparqlConnection.get (None)
    cursor = conn.query(album_query, None)
    while cursor.next (None):
        album_store.append((cursor.get_string(0)[0],))
        print unicode(cursor.get_string(1)[0], "utf-8"), cursor.get_string(0)[0]
        print md5.new(
            cursor.get_string(1)[0] + "\t" + cursor.get_string(0)[0]
        ).hexdigest()

    Gtk.main()
