# -*- coding: utf-8 -*-


# This file defines the dialog for selecting which dates to import.


# Import GTK for the dialog.
from gi.repository import Gtk
# Import the application constants.
from weatherlog_resources.constants import *


class ImportSelectionDialog(Gtk.Dialog):
    """Shows the import selection dialog."""
    
    def __init__(self, parent, title, dates):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 300)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Import All", DialogResponse.IMPORT_ALL)
        self.add_button("Import", DialogResponse.IMPORT)
        
        # Create the frame.
        sel_frame = Gtk.Frame()
        sel_frame.set_label("Select dates to import: ")
        self.get_content_area().add(sel_frame)
        
        # Create the Date selection.
        self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Dates", pro_text, text = 0)
        self.treeview.append_column(self.pro_col)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_frame.add(scrolled_win)
        
        # Add the dates.
        for i in dates:
            self.liststore.append([i])
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = DialogResponse.IMPORT)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
