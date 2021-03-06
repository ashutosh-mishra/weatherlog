# -*- coding: utf-8 -*-


# This file defines the dialog for exporting to Pastebin.


# Import GTK for the dialog.
from gi.repository import Gtk


class ExportPastebinDialog(Gtk.Dialog):
    """Shows the "Export to Pastebin" dialog."""
    
    def __init__(self, parent, title):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        nam_box = self.get_content_area()
        nam_grid = Gtk.Grid()
        nam_box.add(nam_grid)
        
        # Create the labels and entries.
        nam_lbl = Gtk.Label("Paste name: ")
        nam_lbl.set_alignment(0, 0.5)
        nam_grid.add(nam_lbl)
        self.nam_ent = Gtk.Entry()
        nam_grid.attach_next_to(self.nam_ent, nam_lbl, Gtk.PositionType.RIGHT, 1, 1)
        for_lbl = Gtk.Label("Format: ")
        for_lbl.set_alignment(0, 0.5)
        nam_grid.attach_next_to(for_lbl, nam_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.for_com = Gtk.ComboBoxText()
        for i in ["JSON", "HTML", "CSV"]:
            self.for_com.append_text(i)
        self.for_com.set_active(0)
        nam_grid.attach_next_to(self.for_com, for_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
