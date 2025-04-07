
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
     QWidget, QVBoxLayout,  QLabel, QLineEdit, QPushButton, QFrame, QSplitter, QTreeWidget
)


from actions import select_file, update_button_style, launch_analysis, stop_worker_if_exists, update_elapsed_time
from worker import AnalysisWorker

def create_main_widget(main_window):
    """Creates the main widget layout and returns it."""
    
    splitter = QSplitter()

    # Left Side Layout (Inputs & Buttons)
    left_layout = QVBoxLayout()

    # Text input field
    main_window.folder_name_input = QLineEdit()
    main_window.folder_name_input.setPlaceholderText("Enter filename or browse...")
    main_window.folder_name_input.textChanged.connect(lambda: update_button_style(main_window))
    # Browse button
    main_window.browse_button = QPushButton("Browse")
    main_window.browse_button.clicked.connect(lambda: select_file(main_window))

    main_window.stop_button = QPushButton("Stop analysis")
    main_window.stop_button.setStyleSheet("""
        QPushButton[active="false"] {
            background-color: #d3d3d3;  /* Disabled gray */
            color: gray;
            border: solid;
        }

        QPushButton[active="true"] {
            background-color: red;
            color: white;
            font-weight: bold;
            border: solid #a9a9a9;
        }

        QPushButton:pressed {
            color: gray;
            font-weight: bold;
            background-color: darkred;
        }
    """)
    
    main_window.stop_button.clicked.connect(lambda: stop_worker_if_exists(main_window))

    # Launch Analysis button
    main_window.launch_button = QPushButton("Launch Processing")
    main_window.launch_button.setStyleSheet("""
        QPushButton {
            background-color: #f0f0f0;  /* Default gray */
            border: 2px solid #d3d3d3; /* Soft border */
            border-radius: 5px; /* Rounded corners */
            padding: 5px;
        }
        
        QPushButton[active="false"] {
            background-color: #d3d3d3;  /* Disabled gray */
            color: gray;
            border: 2px solid #a9a9a9;
        }

        QPushButton[active="true"] {
            background-color: lightgreen;
            color: darkgreen;
            font-weight: bold;
            border: 2px solid #008000;  /* Dark green border */
        }

        QPushButton:pressed {
            color: lightgreen;
            background-color: #90ee90;  /* Lighter green when clicked */
        }
    """)
    main_window.launch_button.clicked.connect(lambda: launch_analysis(main_window))
    update_button_style(main_window)

    main_window.separator = QFrame(main_window)
    main_window.separator.setFrameShape(QFrame.Shape.HLine)  # Horizontal line
    main_window.separator.setFrameShadow(QFrame.Shadow.Sunken)

    main_window.status_label = QLabel("")  # Initially empty
    main_window.status_label.setStyleSheet("color: grey;")  # Optional styling

    button_layout = QVBoxLayout()
    button_layout.addWidget(main_window.browse_button)
    button_layout.addWidget(main_window.launch_button)
    button_layout.addWidget(main_window.stop_button)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Keep buttons centered


    # Add widgets to left layout
    left_layout.addWidget(main_window.folder_name_input)
    left_layout.addLayout(button_layout)
    left_layout.addStretch(1) 
    left_layout.addWidget(main_window.separator)
    left_layout.addWidget(main_window.status_label)

    left_widget = QWidget()
    left_widget.setLayout(left_layout)
    # left_widget.setFixedWidth(200)

    # Vertical Line Separator
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.VLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)

    # Right Side Layout (Table)
    right_layout = QVBoxLayout()

    main_window.folder_label = QLabel("Analyzed Folder:")

    main_window.results_tree = QTreeWidget()
    main_window.results_tree.setColumnCount(4)
    main_window.results_tree.setHeaderLabels(["Type", "Name", "Size", "Duplicate Locations"])
    main_window.results_tree.setRootIsDecorated(False)  # Hide the default expansion indicator
    main_window.results_tree.setMinimumWidth(415)
    main_window.results_tree.setColumnWidth(0, 35) # type column is narrow
    main_window.results_tree.setColumnWidth(2, 35) # size column is also narrow
    main_window.results_tree.setSortingEnabled(True)

    right_layout.addWidget(main_window.folder_label)
    right_layout.addWidget(main_window.results_tree)

    right_widget = QWidget()
    right_widget.setLayout(right_layout)

    # Add widgets to main layout
    splitter.addWidget(left_widget)
    splitter.addWidget(right_widget)
    splitter.setStretchFactor(0, 0)  # Left panel stays minimal
    splitter.setStretchFactor(1, 1)
    
    
    # Main Layout
    main_layout = QVBoxLayout()
    main_layout.addWidget(splitter)

    # Set main layout
    main_window.setLayout(main_layout)
    main_window.setWindowTitle("Analysis Tool")

    main_window.analysis_timer = QTimer()
    main_window.analysis_timer.setInterval(1000)  # 1000 ms = 1 second
    main_window.analysis_timer.timeout.connect(lambda: update_elapsed_time(main_window))
    main_window.analysis_start_time = None


    return main_layout