import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QVBoxLayout, QPushButton
import folium, io, json, sys, math, random, os
import psycopg2
from folium.plugins import Draw, MousePosition, MeasureControl
from jinja2 import Template
from branca.element import Element
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import (QtGui, QtCore, QtWidgets)

class CitySelectorDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sélection de la ville")
        self.setGeometry(150, 150, 400, 200)  # Définir la taille de la boîte de dialogue

        # Utilisation de feuilles de style pour définir les couleurs et autres propriétés
        self.setStyleSheet("""
            QDialog {
                background-color: #555; /* Gris foncé */
                color: white; /* Couleur du texte */
            }

            QComboBox {
                background-color: #777; /* Gris un peu plus foncé */
                color: white; /* Couleur du texte */
                border: 1px solid #777; /* Bordure */
                border-radius: 4px; /* Coins arrondis */
                padding: 2px;
            }

            QPushButton {
                background-color: #45a049; /* Vert légèrement plus foncé */
                color: white; /* Couleur du texte */
                border: 1px solid #45a049; /* Bordure */
                border-radius: 4px; /* Coins arrondis */
                padding: 5px 10px; /* Espacement du texte à l'intérieur du bouton */
            }
            
            QPushButton:hover {
                background-color: #357e3d; /* Changement de couleur au survol */
            }
        """)

        self.setLayout(QVBoxLayout())

        self.city_combobox = QComboBox()
        self.city_combobox.addItems(["Toulouse", "Paris"])
        self.layout().addWidget(self.city_combobox)

        confirm_button = QPushButton("Confirmer")
        confirm_button.clicked.connect(self.accept)
        self.layout().addWidget(confirm_button)
        
class ToulouseWindow(QMainWindow):

    def __init__(self):
    
        super().__init__()

        self.resize(600, 600)
	
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)

        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)
        self.rows = []
	
        self.webView = myWebView(self)
		
        controls_panel = QHBoxLayout()
        
        mysplit = QSplitter(Qt.Horizontal)
        mysplit.addWidget(self.tableWidget)
        
        map_widget = QWidget() 
        map_layout = QVBoxLayout(map_widget)
        map_layout.addWidget(self.webView)
        map_layout.setContentsMargins(10, 10, 10, 10)
        mysplit.addWidget(map_widget)
        mysplit.setSizes([100, 200])
        controls_and_map_layout = QVBoxLayout()
        controls_and_map_layout.addLayout(controls_panel)
        controls_and_map_layout.addWidget(mysplit)
        main.layout().addLayout(controls_and_map_layout)
        

        _label = QLabel('From: ', self)
        _label.setFixedSize(30,20)
        self.from_box = QComboBox() 
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)

        _label = QLabel('To: ', self)
        _label.setFixedSize(20,20)
        self.to_box = QComboBox() 
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)

        _label = QLabel('Hops: ', self)
        _label.setFixedSize(20,20)
        self.hop_box = QComboBox() 
        self.hop_box.addItems( ['1', '2', '3', '4', '5'] )
        self.hop_box.setCurrentIndex( 2 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.hop_box)


        _label = QLabel('route_type: ', self)
        _label.setFixedSize(20,20)
        self.route_type_box = QComboBox() 
        self.route_type_box.addItems( ['Bus', 'Tram', 'Subway', 'Bus-Tram', 'Bus-Subway', 'Tram-Subway', 'All'] )
        self.route_type_box.setCurrentIndex( 6 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.route_type_box)

        self.go_button = QPushButton("Go!")
        self.go_button.clicked.connect(self.button_Go)
        controls_panel.addWidget(self.go_button)
           
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.button_Clear)
        controls_panel.addWidget(self.clear_button)

        self.setStyleSheet("""
    QMainWindow {
        background-color: #555; /* Gris foncé */
        color: white; /* Couleur du texte */
    }
         """)


        self.go_button.setStyleSheet("""
    QPushButton {
        background-color: #45a049; /* Vert légèrement plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #45a049; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 5px 10px; /* Espacement du texte à l'intérieur du bouton */
    }
    QPushButton:hover {
        background-color: #357e3d; /* Changement de couleur au survol */
    }
        """)
        self.from_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)
        self.to_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)
        self.hop_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)

        self.route_type_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)
       

        self.maptype_box = QComboBox()
        self.maptype_box.addItems(self.webView.maptypes)
        self.maptype_box.currentIndexChanged.connect(self.webView.setMap)
        controls_panel.addWidget(self.maptype_box)
           
        self.connect_DB()

        self.startingpoint = True
        self.clickCount = 0        
        self.show()
        

    def connect_DB(self):
        self.conn = psycopg2.connect(database="name_of_your_data_base", user="your_user_name", host="local_host", password="your_password")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT distinct name FROM network_nodes ORDER BY name""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        for row in rows : 
            self.from_box.addItem(str(row[0]))
            self.to_box.addItem(str(row[0]))


    def table_Click(self):
        k = 0
        prev_lat = 0
        for col in self.rows[self.tableWidget.currentRow()] :
            if (k % 3) == 0:
                lst = col.split(',')
                lat = float(lst[0])
                lon = float(lst[1]) 

                if prev_lat != 0:
                    self.webView.addSegment( prev_lat, prev_lon, lat, lon )
                prev_lat = lat
                prev_lon = lon

                self.webView.addMarker( lat, lon )
            k = k + 1
        

    def button_Go(self):
        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = int(self.hop_box.currentText())
        _route_type = str(self.route_type_box.currentText())

        self.rows = []

        if _hops >= 1 and _route_type == 'All' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, ROUND(A.duration_avg::numeric, 2) AS d_avg FROM (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.from_stop_I = network_nodes.stop_I  AND routes_toulouse.route_I = network_combined.route_I_counts) AS A, (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.to_stop_I = network_nodes.stop_I AND routes_toulouse.route_I = network_combined.route_I_counts) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 1 and _route_type == 'Bus' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, ROUND(A.duration_avg::numeric, 2)  AS d_avg FROM (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.from_stop_I = network_nodes.stop_I  AND routes_toulouse.route_I = network_combined.route_I_counts AND network_combined.route_type = 3 AND routes_toulouse.route_type = 3) AS A, (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.to_stop_I = network_nodes.stop_I AND routes_toulouse.route_I = network_combined.route_I_counts AND network_combined.route_type = 3 AND routes_toulouse.route_type = 3) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 1 and _route_type == 'Tram' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, ROUND(A.duration_avg::numeric, 2)  AS d_avg FROM (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.from_stop_I = network_nodes.stop_I  AND routes_toulouse.route_I = network_combined.route_I_counts AND network_combined.route_type = 0 AND routes_toulouse.route_type = 0) AS A, (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.to_stop_I = network_nodes.stop_I AND routes_toulouse.route_I = network_combined.route_I_counts AND network_combined.route_type = 0 AND routes_toulouse.route_type = 0) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 1 and _route_type == 'Subway' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, ROUND(A.duration_avg::numeric, 2)  AS d_avg FROM (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.from_stop_I = network_nodes.stop_I  AND routes_toulouse.route_I = network_combined.route_I_counts AND network_combined.route_type = 1 AND routes_toulouse.route_type = 1) AS A, (SELECT * FROM network_combined,network_nodes,routes_toulouse WHERE network_combined.to_stop_I = network_nodes.stop_I AND routes_toulouse.route_I = network_combined.route_I_counts AND network_combined.route_type = 1 AND routes_toulouse.route_type = 1) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 2 and _route_type == 'All': 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, C.route_name,D.name, NULL, NULL, A.d + C.d, ROUND((A.duration_avg + C.duration_avg)::numeric, 2) as d_avg FROM (SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_I = network_nodes.stop_I AND routes_toulouse.route_I = network_combined.route_I_counts) AS A, (SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_I = network_nodes.stop_I AND routes_toulouse.route_I = network_combined.route_I_counts) AS B, (SELECT * FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_I = network_nodes.stop_I  AND routes_toulouse.route_I = network_combined.route_I_counts) AS C, (SELECT * FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.to_stop_I = network_nodes.stop_I AND routes_toulouse.route_i = network_combined.route_I_counts ) AS D WHERE A.name = $${_fromstation}$$  AND D.name = $${_tostation}$$ AND A.route_I_counts = B.route_I_counts AND B.name = C.name  AND C.route_i_counts = D.route_i_counts AND A.route_i_counts <> C.route_i_counts  AND A.name <> B.name   AND B.name <> D.name ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 3 and _route_type == 'All' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B2.name, B2.route_name, C2.name, C2.route_name, D.name, (A.d + B2.d + C2.d) as dist, ROUND((A.duration_avg + B2.duration_avg + C2.duration_avg)::numeric, 2) as d_avg FROM (SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_i = network_nodes.stop_i AND routes_toulouse.route_i = network_combined.route_i_counts) AS A, (SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_i = network_nodes.stop_i AND routes_toulouse.route_i = network_combined.route_i_counts) AS B1,(SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_i = network_nodes.stop_i AND routes_toulouse.route_i = network_combined.route_i_counts) AS B2,(SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_i = network_nodes.stop_i AND routes_toulouse.route_i = network_combined.route_i_counts) AS C1, (SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_i = network_nodes.stop_i AND routes_toulouse.route_i = network_combined.route_i_counts) AS C2, (SELECT *FROM network_combined, network_nodes, routes_toulouse WHERE network_combined.from_stop_i = network_nodes.stop_i AND routes_toulouse.route_i = network_combined.route_i_counts) AS D WHERE A.name = $${_fromstation}$$ AND A.route_i_counts = B1.route_i_counts AND B1.name = B2.name AND B2.route_i_counts = C1.route_i_counts AND C1.name = C2.name AND C2.route_i_counts = D.route_i_counts AND D.name = $${_tostation}$$ AND A.route_i_counts <> B2.route_i_counts AND B2.route_i_counts <> C2.route_i_counts AND A.route_i_counts <> C2.route_i_counts AND A.name <> B1.name AND B2.name <> C1.name AND C2.name <> D.name ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()
        

        if len(self.rows) == 0 : 
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        
        self.tableWidget.setRowCount(len(self.rows))
        self.tableWidget.setColumnCount(len(self.rows[-1]))

        i = 0
        for row in self.rows : 
            j = 0
            for col in row :
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))
                j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < len(self.rows[-1]) :
            header.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)
            j = j+1
        
        self.update()	


    def button_Clear(self):
        self.webView.clearMap(self.maptype_box.currentIndex())
        self.startingpoint = True
        self.update()


    def mouseClick(self, lat, lng):
        self.webView.addPointMarker(lat, lng)

        print(f"Clicked on: latitude {lat}, longitude {lng}")
        self.cursor.execute(""f" WITH stations AS (SELECT A.name, (A.lat - {lat}) * (A.lat - {lat}) + (A.lon - {lng})*(A.lon - {lng}) AS distance FROM network_nodes AS A) SELECT T.name FROM (SELECT A.name, (A.lat - {lat}) * (A.lat - {lat}) + (A.lon - {lng})*(A.lon - {lng}) AS distance FROM network_nodes as A) as T where T.distance <= ALL (SELECT distance from stations) """)

        self.conn.commit()
        rows = self.cursor.fetchall()
        #print('Closest STATION is: ', rows[0][0])
        if self.startingpoint :
            self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
        else :
            self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
        self.startingpoint = not self.startingpoint



class ParisWindow(QMainWindow):

    def __init__(self):
    
        super().__init__()
        self.resize(600, 600)
	
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)

        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)
        self.rows = []
	
        self.webView = myWebView(self)
		
        controls_panel = QHBoxLayout()
        
        mysplit = QSplitter(Qt.Horizontal)
        mysplit.addWidget(self.tableWidget)
        
        map_widget = QWidget() 
        map_layout = QVBoxLayout(map_widget)
        map_layout.addWidget(self.webView)
        map_layout.setContentsMargins(10, 10, 10, 10)
        mysplit.addWidget(map_widget)
        mysplit.setSizes([100, 200])
        controls_and_map_layout = QVBoxLayout()
        controls_and_map_layout.addLayout(controls_panel)
        controls_and_map_layout.addWidget(mysplit)
        main.layout().addLayout(controls_and_map_layout)
        

        _label = QLabel('From: ', self)
        _label.setFixedSize(30,20)
        self.from_box = QComboBox() 
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)

        _label = QLabel('To: ', self)
        _label.setFixedSize(20,20)
        self.to_box = QComboBox() 
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)

        _label = QLabel('Hops: ', self)
        _label.setFixedSize(20,20)
        self.hop_box = QComboBox() 
        self.hop_box.addItems( ['1', '2', '3', '4', '5'] )
        self.hop_box.setCurrentIndex( 2 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.hop_box)


        _label = QLabel('route_type: ', self)
        _label.setFixedSize(20,20)
        self.route_type_box = QComboBox() 
        self.route_type_box.addItems( ['Bus', 'Tram', 'Subway', 'Bus-Tram', 'Bus-Subway', 'Tram-Subway', 'All'] )
        self.route_type_box.setCurrentIndex( 6 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.route_type_box)

        self.go_button = QPushButton("Go!")
        self.go_button.clicked.connect(self.button_Go)
        controls_panel.addWidget(self.go_button)
           
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.button_Clear)
        controls_panel.addWidget(self.clear_button)

        self.setStyleSheet("""
    QMainWindow {
        background-color: #555; /* Gris foncé */
        color: white; /* Couleur du texte */
    }
         """)


        self.go_button.setStyleSheet("""
    QPushButton {
        background-color: #45a049; /* Vert légèrement plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #45a049; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 5px 10px; /* Espacement du texte à l'intérieur du bouton */
    }
    QPushButton:hover {
        background-color: #357e3d; /* Changement de couleur au survol */
    }
        """)
        self.from_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)
        self.to_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)
        self.hop_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)

        self.route_type_box.setStyleSheet("""
    QComboBox {
        background-color: #777; /* Gris un peu plus foncé */
        color: white; /* Couleur du texte */
        border: 1px solid #777; /* Bordure */
        border-radius: 4px; /* Coins arrondis */
        padding: 2px;
    }
        """)
       

        self.maptype_box = QComboBox()
        self.maptype_box.addItems(self.webView.maptypes)
        self.maptype_box.currentIndexChanged.connect(self.webView.setMap)
        controls_panel.addWidget(self.maptype_box)
           
        self.connect_DB()

        self.startingpoint = True
        self.clickCount = 0        
        self.show()
        

    def connect_DB(self):
        self.conn = psycopg2.connect(database="l3info_11", user="l3info_11", host="10.11.11.22", password="L3INFO_11")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT distinct name FROM network_nodes_p ORDER BY name""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        for row in rows : 
            self.from_box.addItem(str(row[0]))
            self.to_box.addItem(str(row[0]))


    def table_Click(self):
        k = 0
        prev_lat = 0
        for col in self.rows[self.tableWidget.currentRow()] :
            if (k % 3) == 0:
                lst = col.split(',')
                lat = float(lst[0])
                lon = float(lst[1]) 

                if prev_lat != 0:
                    self.webView.addSegment( prev_lat, prev_lon, lat, lon )
                prev_lat = lat
                prev_lon = lon

                self.webView.addMarker( lat, lon )
            k = k + 1
        

    def button_Go(self):
        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = int(self.hop_box.currentText())
        _route_type = str(self.route_type_box.currentText())

        self.rows = []

        if _hops >= 1 and _route_type == 'All' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, round(A.duration_avg::numeric,2) AS d_avg FROM (SELECT * FROM network_combined_p,network_nodes_p,routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I  AND routes_paris.route_I = network_combined_p.route_I_counts) AS A, (SELECT * FROM network_combined_p,network_nodes_p,routes_paris WHERE network_combined_p.to_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 1 and _route_type == 'Bus' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, round(A.duration_avg::numeric,2) AS d_avg FROM (SELECT * FROM network_combined_p,network_nodes_p,routes_pari WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I  AND routes_paris.route_I = network_combined_p.route_I_counts AND network_combined_p.route_type = 3 AND routes_paris.route_type = 3) AS A, (SELECT * FROM network_combined_p,network_nodes_p,routes_paris WHERE network_combined_p.to_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts AND network_combined_p.route_type = 3 AND routes_paris.route_type = 3) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 1 and _route_type == 'Tram' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, round(A.duration_avg::numeric,2) AS d_avg FROM (SELECT * FROM network_combined_p,network_nodes_p,routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I  AND routes_paris.route_I = network_combined_p.route_I_counts AND network_combined_p.route_type = 0 AND routes_paris.route_type = 0) AS A, (SELECT * FROM network_combined_p,network_nodes_p,routes_paris WHERE network_combined_p.to_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts AND network_combined_p.route_type = 0 AND routes_paris.route_type = 0) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 1 and _route_type == 'Subway' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, NULL, NULL, NULL, NULL, A.d, round(A.duration_avg::numeric,2) AS d_avg FROM (SELECT * FROM network_combined_p,network_nodes_p,routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I  AND routes_paris.route_I = network_combined_p.route_I_counts AND network_combined_p.route_type = 1 AND routes_paris.route_type = 1) AS A, (SELECT * FROM network_combined_p,network_nodes_p,routes_paris WHERE network_combined_p.to_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts AND network_combined_p.route_type = 1 AND routes_paris.route_type = 1) AS B WHERE A.name= $${_fromstation}$$ AND B.name= $${_tostation}$$ AND A.route_I_counts = B.route_I_counts ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 2 and _route_type == 'All': 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B.name, C.route_name,D.name, NULL, NULL, A.d + C.d, round((A.duration_avg + C.duration_avg)::numeric, 2) as d_avg FROM (SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS A, (SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS B, (SELECT * FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I  AND routes_paris.route_I = network_combined_p.route_I_counts) AS C, (SELECT * FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.to_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts ) AS D WHERE A.name = $${_fromstation}$$  AND D.name = $${_tostation}$$ AND A.route_I_counts = B.route_I_counts AND B.name = C.name  AND C.route_I_counts = D.route_I_counts AND A.route_I_counts <> C.route_I_counts  AND A.name <> B.name   AND B.name <> D.name ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 3 and _route_type == 'All' : 
            self.cursor.execute(""f" SELECT distinct A.name, A.route_name, B2.name, B2.route_name, C2.name, C2.route_name, D.name, (A.d + B2.d + C2.d) as dist, round((A.duration_avg + B2.duration_avg + C2.duration_avg)::numeric, 2) as d_avg FROM (SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS A, (SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS B1,(SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS B2,(SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS C1, (SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS C2, (SELECT *FROM network_combined_p, network_nodes_p, routes_paris WHERE network_combined_p.from_stop_I = network_nodes_p.stop_I AND routes_paris.route_I = network_combined_p.route_I_counts) AS D WHERE A.name = $${_fromstation}$$ AND A.route_I_counts = B1.route_I_counts AND B1.name = B2.name AND B2.route_I_counts = C1.route_I_counts AND C1.name = C2.name AND C2.route_I_counts = D.route_I_counts AND D.name = $${_tostation}$$ AND A.route_I_counts <> B2.route_I_counts AND B2.route_I_counts <> C2.route_I_counts AND A.route_I_counts <> C2.route_I_counts AND A.name <> B1.name AND B2.name <> C1.name AND C2.name <> D.name ORDER BY d_avg""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()
        

        if len(self.rows) == 0 : 
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        
        self.tableWidget.setRowCount(len(self.rows))
        self.tableWidget.setColumnCount(len(self.rows[-1]))

        i = 0
        for row in self.rows : 
            j = 0
            for col in row :
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))
                j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < len(self.rows[-1]) :
            header.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)
            j = j+1
        
        self.update()	


    def button_Clear(self):
        self.webView.clearMap(self.maptype_box.currentIndex())
        self.startingpoint = True
        self.update()


    def mouseClick(self, lat, lng):
        self.webView.addPointMarker(lat, lng)

        print(f"Clicked on: latitude {lat}, longitude {lng}")
        self.cursor.execute(""f" WITH stations AS (SELECT A.name, (A.lat - {lat}) * (A.lat - {lat}) + (A.lon - {lng})*(A.lon - {lng}) AS distance FROM network_nodes_p AS A) SELECT T.name FROM (SELECT A.name, (A.lat - {lat}) * (A.lat - {lat}) + (A.lon - {lng})*(A.lon - {lng}) AS distance FROM network_nodes_p as A) as T where T.distance <= ALL (SELECT distance from stations) """)

        self.conn.commit()
        rows = self.cursor.fetchall()
        #print('Closest STATION is: ', rows[0][0])
        if self.startingpoint :
            self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
        else :
            self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
        self.startingpoint = not self.startingpoint



class myWebView (QWebEngineView):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        self.maptypes = ["OpenStreetMap", "Stamen Terrain", "stamentoner", "cartodbpositron"]
        self.setMap(0)


    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}}); """
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        html.script._children[e.get_name()] = e

        return map_object


    def handleClick(self, msg):
        data = json.loads(msg)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']


        self.parent.mouseClick(lat, lng)


    def addSegment(self, lat1, lng1, lat2, lng2):
        js = Template(
        """
        L.polyline(
            [ [{{latitude1}}, {{longitude1}}], [{{latitude2}}, {{longitude2}}] ], {
                "color": "red",
                "opacity": 1.0,
                "weight": 4,
                "line_cap": "butt"
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude1=lat1, longitude1=lng1, latitude2=lat2, longitude2=lng2 )

        self.page().runJavaScript(js)


    def addMarker(self, lat, lng):
        js = Template(
        """
        L.marker([{{latitude}}, {{longitude}}] ).addTo({{map}});
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def addPointMarker(self, lat, lng):
        js = Template(
        """
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": 'green',
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": 'green',
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def setMap (self, i):
        if selected_city == "Paris":
        	self.mymap = folium.Map(location=[48.8666,2.3333], tiles=self.maptypes[i], zoom_start=12, prefer_canvas=True)
        elif selected_city == "Toulouse":
        	self.mymap = folium.Map(location=[43.5999,1.4333], tiles=self.maptypes[i], zoom_start=12, prefer_canvas=True)
        self.mymap = self.add_customjs(self.mymap)

        page = WebEnginePage(self)
        self.setPage(page)

        data = io.BytesIO()
        self.mymap.save(data, close_file=False)

        self.setHtml(data.getvalue().decode())

    def clearMap(self, index):
        self.setMap(index)



class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        #print(msg)
        if 'coordinates' in msg:
            self.parent.handleClick(msg)

if __name__ == "__main__":
    app = QApplication([])

    city_selector_dialog = CitySelectorDialog()
    if city_selector_dialog.exec_() == QDialog.Accepted:
        selected_city = city_selector_dialog.city_combobox.currentText()

        if selected_city == "Toulouse":
            toulouse_window = ToulouseWindow()
            toulouse_window.show()
        elif selected_city == "Paris":
            Paris_window = ParisWindow()
            Paris_window.show()

    sys.exit(app.exec_())
