import sys
from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Call the superclass constructor
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        #khai báo các nút
        self.uic.startBtn.clicked.connect(self.generateInputFields)
        self.uic.reQuestBtn.clicked.connect(self.req_click)
        self.uic.noRequestBtn.clicked.connect(self.req_click)
        self.uic.showBtn.clicked.connect(self.run_algorithm)
        self.uic.exBtn.clicked.connect(self.load_example_data)
        self.num_processes = 0  # Make them instance variables
        self.num_resources = 0
        self.avail = None
        self.maxm = None
        self.allot = None
        self.uic.refreshBtn.clicked.connect(self.refresh)

    def generateInputFields(self):
        self.num_processes = int(self.uic.processSpinbox.value())
        self.num_resources = int(self.uic.resourceSpinbox.value())
        self.uic.processcomboBox.clear()
        if self.num_processes <= 0 or self.num_resources <= 0:  # Add "self." to these variables
            QMessageBox.warning(
                None, "Error", "Please enter a number greater than 0")
            return
        try:
            # generate available table
            self.uic.availTable.setColumnCount(self.num_resources)
            self.uic.availTable.setRowCount(1)
            self.uic.availTable.setHorizontalHeaderLabels(
                [f"R{i + 1}" for i in range(self.num_resources)])
            for i in range(self.num_processes):
                for j in range(self.num_resources):
                    self.uic.availTable.setItem(i, j, QtWidgets.QTableWidgetItem("0"))
            self.uic.availTable.setVerticalHeaderLabels(["Available"])

            # generate max table with default values of 0
            self.uic.maxTable.setColumnCount(self.num_resources)
            self.uic.maxTable.setRowCount(self.num_processes)
            self.uic.maxTable.setHorizontalHeaderLabels(
                [f"R{i + 1}" for i in range(self.num_resources)])
            self.uic.maxTable.setVerticalHeaderLabels(
                [f"P{i}" for i in range(self.num_processes)])
            for i in range(self.num_processes):
                for j in range(self.num_resources):
                    self.uic.maxTable.setItem(i, j, QtWidgets.QTableWidgetItem("0"))

            # generate allocation table with default values of 0
            self.uic.allocationTable.setColumnCount(self.num_resources)
            self.uic.allocationTable.setRowCount(self.num_processes)
            self.uic.allocationTable.setHorizontalHeaderLabels(
                [f"R{i + 1}" for i in range(self.num_resources)])
            self.uic.allocationTable.setVerticalHeaderLabels(
                 [f"P{i}" for i in range(self.num_processes)])
            for i in range(self.num_processes):
                for j in range(self.num_resources):
                    self.uic.allocationTable.setItem(i, j, QtWidgets.QTableWidgetItem("0"))

            # Generate allocation table with default values of 0
            self.uic.needTable.setColumnCount(self.num_resources)
            self.uic.needTable.setRowCount(self.num_processes)
            self.uic.needTable.setHorizontalHeaderLabels(
                [f"R{i + 1}" for i in range(self.num_resources)])
            self.uic.needTable.setVerticalHeaderLabels(
                [f"P{i}" for i in range(self.num_processes)])
            for i in range(self.num_processes):
                for j in range(self.num_resources):
                    self.uic.needTable.setItem(i, j, QtWidgets.QTableWidgetItem("0"))

            self.uic.availTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.uic.requestTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.uic.maxTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.uic.allocationTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.uic.needTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        except Exception as e:
            print(f"An error occurred: {e}")

    def req_click(self):
            if self.uic.reQuestBtn.isChecked():
                self.uic.requestTable.setVisible(True)
                self.uic.requestmatrixLabel.setVisible(True)
                self.uic.process.setVisible(True)
                self.uic.processcomboBox.setVisible(True)
                self.uic.processcomboBox.setVisible(True)

                try:
                    self.uic.requestTable.setColumnCount(self.num_resources)
                    self.uic.requestTable.setRowCount(1)
                    self.uic.requestTable.setHorizontalHeaderLabels(
                        [f"R{i + 1}" for i in range(self.num_resources)])
                    for i in range(self.num_processes):
                        for j in range(self.num_resources):
                            self.uic.requestTable.setItem(i, j, QtWidgets.QTableWidgetItem("0"))
                    self.uic.requestTable.setVerticalHeaderLabels(["Request"])
                except Exception as e:
                    print(f"An error occurred: {e}")

                for i in range(self.num_processes):
                    self.uic.processcomboBox.addItem(f'P{i}')

            elif self.uic.noRequestBtn.isChecked():
                self.uic.requestTable.setVisible(False)
                self.uic.requestmatrixLabel.setVisible(False)
                self.uic.process.setVisible(False)
                self.uic.processcomboBox.setVisible(False)
                self.uic.processcomboBox.clear()
            else:
                return
    def run_algorithm(self):
        self.uic.workTab.clear()
        self.uic.showResult.clear()
        try:
            # Check if all values are positive numbers only in the available table
            for i in range(self.uic.availTable.columnCount()):
                if not self.uic.availTable.item(0, i).text().isnumeric():
                    QMessageBox.warning(
                        None, "Error", "Available table values must be POSITIVE numbers only")
                    return
            # Check if all values are positive numbers only in the max table
            for i in range(self.uic.maxTable.columnCount()):
                if not self.uic.maxTable.item(0, i).text().isnumeric():
                    QMessageBox.warning(
                        None, "Error", "Max table values must be POSITIVE numbers only")
                    return
            # Check if all values are positive numbers only in the allocation table
            for i in range(self.uic.allocationTable.columnCount()):
                if not self.uic.allocationTable.item(0, i).text().isnumeric():
                    QMessageBox.warning(
                        None, "Error", "Allocation table values must be POSITIVE numbers only")
                    return
            # get available table values
            available = []
            for i in range(self.uic.availTable.columnCount()):
                available.append(int(self.uic.availTable.item(0, i).text()))
            #get max
            max = []
            for i in range(int(self.num_processes)):
                max.append([])
                for j in range(int(self.num_resources)):
                    max[i].append(
                        int(self.uic.maxTable.item(i, j).text()))
            #get allocation
            allocation = []
            for i in range(int(self.num_processes)):
                allocation.append([])
                for j in range(int(self.num_resources)):
                    allocation[i].append(
                        int(self.uic.allocationTable.item(i, j).text()))
            #get request
            request = []
            for i in range(self.uic.requestTable.columnCount()):
                request.append(int(self.uic.requestTable.item(0, i).text()))

            print("available:",available)
            print("Allocation:",allocation)
            print("Max Table:",max)
            print("Request table:",request)

        except Exception as e:
            print(f"Error: {e}")

        if self.uic.reQuestBtn.isChecked():
            self.request_resources(allocation, max, available, request)
        else:
            self.safe_sequence(available, max, allocation)

    def safe_sequence(self, available, max, allocation):
        try:
            finish = [False] * self.num_processes
            work = available.copy()  # Bước 1: Khởi tạo work = available
            safe_sequence = []
            need =[]
            for i in range(self.num_processes):
                need.append([])
                for j in range(self.num_resources):
                    need[i].append(max[i][j] - allocation[i][j])
            for i in range(self.num_processes):
                for j in range(self.num_resources):
                    self.uic.needTable.setItem(i,j,QtWidgets.QTableWidgetItem(str(need[i][j])))

            while len(safe_sequence) < self.num_processes:  # Chỉ cần tìm chuỗi an toàn cho tất cả quá trình
                found = False
                for i in range(self.num_processes):
                    if not finish[i]:
                        # So sánh từng tài nguyên cụ thể cho quá trình i
                        resource_enough = True
                        for j in range(self.num_resources):
                            if need[i][j] > work[j]:
                                resource_enough = False
                                break
                        if resource_enough:
                            # Có thể cấp tài nguyên cho quá trình i
                            for j in range(self.num_resources):
                                work[j] += allocation[i][j]
                            finish[i] = True
                            safe_sequence.append(i)
                            found = True
                            break
                if not found:
                    self.uic.showResult.append("No safe sequence found")

                    return None  # Không tìm thấy chuỗi an toàn
                self.uic.workTab.append(f"Work after allocating resources for process {i} : {work}")
            self.uic.showResult.append(f"Safe sequence: {' -> '.join([f'P{i}' for i in safe_sequence])}")
            return safe_sequence
        except Exception as e:
            print(f"Error in safe_sequence: {e}")
    def request_resources(self, allocation, max, available, request):
        try:
            # Kiểm tra xem yêu cầu có hợp lệ không
            for i in range(self.num_resources):
                if request[i] > max[self.uic.processcomboBox.currentIndex()][i] - \
                        allocation[self.uic.processcomboBox.currentIndex()][i]:
                    QMessageBox.warning(
                        None, "Error","Process requests more than its max claim.")
                    return
            # Tạo một bản sao tạm thời của tài nguyên để kiểm tra tài nguyên sau khi yêu cầu
            temp_available = available.copy()
            temp_allocation = allocation.copy()
            temp_need = []

            for i in range(self.num_processes):
                temp_need.append([])
                for j in range(self.num_resources):
                    temp_need[i].append(max[i][j] - allocation[i][j])
            # Kiểm tra xem yêu cầu có thể được thực hiện không
            for i in range(self.num_resources):
                if request[i] > temp_available[i]:
                    QMessageBox.warning(
                        None, "Error","Resources not available for request.")
                    return
            # Thực hiện tạm thời cập nhật các bảng
            for i in range(self.num_resources):
                temp_available[i] -= request[i]
                temp_allocation[self.uic.processcomboBox.currentIndex()][i] += request[i]
                temp_need[self.uic.processcomboBox.currentIndex()][i] -= request[i]
            # Kiểm tra xem tạm thời có chuỗi an toàn không
            safe_sequence = self.safe_sequence(temp_available, max, temp_allocation)

          
            if safe_sequence:
                # Nếu có chuỗi an toàn, thực hiện cập nhật tài nguyên thực tế
                available2 = temp_available
                allocation2 = temp_allocation
                need2 = temp_need
                self.uic.showResult.append("Resource request granted.")
                # Cập nhật bảng Need trong cửa sổ con
                for i in range(self.num_processes):
                    for j in range(self.num_resources):
                        self.uic.needTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(need2[i][j])))
                # Cập nhật bảng Allocation trong cửa sổ con
                for i in range(self.num_processes):
                    for j in range(self.num_resources):
                        self.uic.allocationTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(allocation2[i][j])))
                    # Highlight the requested row in the Allocation table
                process_index = self.uic.processcomboBox.currentIndex()
                for i in range(self.num_resources):
                    self.uic.allocationTable.item(process_index, i).setBackground(
                        QtGui.QColor(0, 255, 0))  # Green background

                    # Highlight the requested row in the Need table
                for i in range(self.num_resources):
                    self.uic.needTable.item(process_index, i).setBackground(
                        QtGui.QColor(0, 255, 0))  # Green background
            else:
                QMessageBox.warning(
                    None, "Error","Resource request denied. Unsafe state.")
        except Exception as e:
            print(f"Error in request_resources: {e}")
    def refresh(self):
        # Reset the values to their initial state
        self.num_processes = 0
        self.num_resources = 0
        self.avail = None
        self.maxm = None
        self.allot = None

        # Reset the input fields and tables
        self.uic.processSpinbox.setValue(0)
        self.uic.resourceSpinbox.setValue(0)
        self.uic.requestTable.setVisible(False)
        self.uic.requestmatrixLabel.setVisible(False)
        self.uic.process.setVisible(False)
        self.uic.processcomboBox.setVisible(False)
        self.uic.processcomboBox.clear()
        self.uic.showResult.clear()
        self.uic.workTab.clear()
        self.uic.availTable.clear()
        self.uic.maxTable.clear()
        self.uic.allocationTable.clear()
        self.uic.needTable.clear()
        self.uic.requestTable.clear()
    def load_example_data(self):
        allocation_data = [
            [4, 1, 2],
            [4, 3, 2],
            [3, 2, 4],
            [1, 4, 1],
            [2, 2, 3]
        ]

        max_data = [
            [11, 8, 5],
            [9, 6, 4],
            [7, 4, 5],
            [10, 7, 4],
            [8, 5, 6]
        ]

        available_data = [7, 3, 3]

        # Set data for Allocation table
        for i in range(len(allocation_data)):
            for j in range(len(allocation_data[0])):
                self.uic.allocationTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(allocation_data[i][j])))

        # Set data for Max table
        for i in range(len(max_data)):
            for j in range(len(max_data[0])):
                self.uic.maxTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(max_data[i][j])))

        # Set data for Available table
        for i in range(len(available_data)):
            self.uic.availTable.setItem(0, i, QtWidgets.QTableWidgetItem(str(available_data[i])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
