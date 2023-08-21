import customtkinter as ctk
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import pandas as pd
from kafka import KafkaProducer
import json
from privacy.privacy import privacy

ctk.set_appearance_mode("light")


try:
    producer = KafkaProducer(
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"],
    )
except:
    pass


pharmacy_entries = None
hospital_entries = {"heartdisease": {}, "diabetes": {}}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # DEFAULT OPTIONS
        self.dataset = "symptoms"
        self.method = "k-anonymity"
        self.dataframe = None

        self.title("Streamly")
        self.minsize(1000, 650)
        self.create_intro_page()
        # self.create_main_page()
        self.mainloop()

    def create_intro_page(self):
        # create the frame of page
        self.frame = ctk.CTkFrame(master=self, fg_color="#fff")
        self.frame.pack(expand=True, fill="both")
        # create the container of the widgets of first page
        container = ctk.CTkFrame(master=self.frame, fg_color="transparent")
        container.pack(expand=True)
        # place the widgets in the container
        # 1 - place the logo
        image = Image.open(f".\\resources\\logo.png").resize((150, 150))
        self.image = ImageTk.PhotoImage(image=image)
        canvas = ctk.CTkCanvas(
            width=150,
            height=150,
            master=container,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.pack()
        canvas.create_image(0, 0, image=self.image, anchor="nw")
        # 2 - place the logo
        label = ctk.CTkLabel(
            master=container,
            text="Stream data, Help people",
            font=("Nico Moji", 24),
            text_color="#36365A",
        )
        label.pack(pady=15)
        # 3 - place the button
        button = ctk.CTkButton(
            master=container,
            text="Start",
            fg_color="#36365A",
            font=("Nico Moji", 18),
            hover_color="#6768AB",
            command=self.create_main_page,
        )
        button.pack(ipady=5, pady=15)

    def create_main_page(self):
        self.frame.destroy()
        # main frame
        self.main = ctk.CTkFrame(master=self)
        self.main.pack(expand=True, fill="both")
        self.main.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.main.rowconfigure(0, weight=1, uniform="b")

        # the tab view widget
        self.tab = ctk.CTkTabview(
            master=self.main, command=self.tab_changed, corner_radius=20
        )
        self.tab.grid(
            row=0, column=0, sticky="nsew", padx=20, pady=10, ipadx=20, ipady=20
        )
        self.tab.add("Pharmacy")
        self.tab.add("Hospital")

        # pharmacy tab
        """
        privacy_type = tk.StringVar(value="k-anonymity")
        k_anonymity = ctk.CTkRadioButton(
            self.tab.tab("Pharmacy"),
            text="K-Anonymity",
            variable=privacy_type,
            value="k-anonymity",
            command=lambda: self.set_method(),
        )
        differential_privacy = ctk.CTkRadioButton(
            self.tab.tab("Pharmacy"),
            text="Differential privacy",
            variable=privacy_type,
            value="differential_privacy",
            command=lambda: self.set_method("differential_privacy"),
        )
        homomorphic_encryption = ctk.CTkRadioButton(
            self.tab.tab("Pharmacy"),
            text="Homomorphic encryption",
            variable=privacy_type,
            value="homomorphic_encryption",
            command=lambda: self.set_method("homomorphic_encryption"),
        )

        k_anonymity.pack(pady=15)
        differential_privacy.pack()
        homomorphic_encryption.pack(pady=15)
        """
        # hospital
        # 1 - methods
        """
        methods = ctk.CTkFrame(master=self.tab.tab("Hospital"), corner_radius=20)
        privacy_type = tk.StringVar(value=self.method)
        k_anonymity = ctk.CTkRadioButton(
            methods,
            text="K-Anonymity",
            variable=privacy_type,
            value="k-anonymity",
            command=lambda: self.set_method(),
        )
        differential_privacy = ctk.CTkRadioButton(
            methods,
            text="Differential privacy",
            variable=privacy_type,
            value="differential_privacy",
            command=lambda: self.set_method("differential_privacy"),
        )
        homomorphic_encryption = ctk.CTkRadioButton(
            methods,
            text="Homomorphic encryption",
            variable=privacy_type,
            value="homomorphic_encryption",
            command=lambda: self.set_method("homomorphic_encryption"),
        )
        k_anonymity.pack(expand=True)
        differential_privacy.pack(expand=True)
        homomorphic_encryption.pack(expand=True)
        methods.pack(ipadx=15, ipady=15, fill="both", expand=True, pady=20)
        """
        # 2 - data type
        datatype_frame = ctk.CTkFrame(master=self.tab.tab("Hospital"), corner_radius=20)
        dataset_var = tk.StringVar(value="heartdisease")
        heart = ctk.CTkRadioButton(
            datatype_frame,
            text="Heart disease",
            value="heartdisease",
            variable=dataset_var,
            command=self.set_dataset,
        )
        Diabetes = ctk.CTkRadioButton(
            datatype_frame,
            text="diabetes",
            value="diabetes",
            variable=dataset_var,
            command=lambda: self.set_dataset(dataset="diabetes"),
        )
        heart.pack(expand=True)
        Diabetes.pack(expand=True)
        datatype_frame.pack(ipadx=15, ipady=15, expand=True, fill="both")
        self.create_pharmacy_frame()

    def create_pharmacy_frame(self):
        global pharmacy_entries
        PHARMACY_FORM = ["UserId", "Name", "Symptoms", "Drug"]
        try:
            self.right_frame.forget_pack()
        except:
            pass
        self.right_frame = ctk.CTkFrame(master=self.main, corner_radius=20)
        self.right_frame.grid(
            row=0, column=1, columnspan=3, sticky="nsew", padx=20, pady=20
        )

        buttons_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        buttons_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")
        buttons_frame.rowconfigure(0, weight=1)
        form_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")

        # create the form
        form_container = ctk.CTkFrame(form_frame)
        form_container.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        form_container.columnconfigure((0, 1, 2), weight=1, uniform="b")

        pharmacy_entries = {}
        for index, input in enumerate(PHARMACY_FORM):
            value = tk.StringVar(value="")
            label = ctk.CTkLabel(form_container, text=input, justify="left")
            label.grid(row=index, column=0, sticky="nsew", pady=20)
            entry = ctk.CTkEntry(form_container, textvariable=value)
            pharmacy_entries[input] = value
            entry.grid(
                row=index, column=1, columnspan=2, sticky="nsew", pady=20, padx=30
            )

        form_container.pack(expand=True, fill="x", padx=150, ipady=20, pady=20)
        form_frame.pack(expand=True, fill="both", ipady=30)

        # create the button frame
        reset = ctk.CTkButton(
            buttons_frame,
            text="Reset",
            fg_color="red",
            command=lambda: self.reset_entries(pharmacy_entries),
        )
        load_csv = ctk.CTkButton(
            buttons_frame,
            text="Stream from csv",
            fg_color="green",
            command=self.read_dataframe,
        )
        stream = ctk.CTkButton(
            buttons_frame,
            text="Stream",
            fg_color="blue",
            command=lambda: self.stream_data(),
        )
        reset.grid(row=0, column=0)
        load_csv.grid(row=0, column=1)
        stream.grid(row=0, column=2)
        buttons_frame.pack(expand=True, fill="x", padx=150)

    def reset_entries(self, entries):
        for input in list(entries.keys()):
            entries[input].set("")

    def create_hospital_frame(self):
        global hospital_entries
        hospital_entries = {"heartdisease": {}, "diabetes": {}}
        DATASET_OPTION = {
            "diabetes": [
                "Pregnancies",
                "Glucose",
                "BloodPressure",
                "SkinThickness",
                "Insulin",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age",
                "Outcome",
            ],
            "heartdisease": [
                "age",
                "sex",
                "cp",
                "trestbps",
                "chol",
                "fbs",
                "restecg",
                "thalach",
                "exang",
                "oldpeak",
                "slope",
                "ca",
                "thal",
                "target",
            ],
        }
        try:
            self.right_frame.grid_forget()
        except:
            pass
        self.right_frame = ctk.CTkFrame(master=self.main)
        self.right_frame.grid(
            row=0, column=1, columnspan=3, sticky="nsew", padx=20, pady=20
        )

        buttons_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        buttons_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")
        buttons_frame.rowconfigure(0, weight=1)
        form_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")

        # create the form
        form_container = ctk.CTkScrollableFrame(form_frame)
        form_container.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        form_container.columnconfigure((0, 1, 2), weight=1, uniform="b")

        entries = {}
        for index, input in enumerate(DATASET_OPTION[self.dataset]):
            value = tk.StringVar(value="")
            hospital_entries[self.dataset][input] = value
            label = ctk.CTkLabel(form_container, text=input, justify="left")
            label.grid(row=index, column=0, sticky="nsew", pady=20)
            entry = ctk.CTkEntry(form_container, textvariable=value)
            entry.grid(
                row=index, column=1, columnspan=2, sticky="nsew", pady=20, padx=30
            )
            entries[input] = value

        form_container.pack(expand=True, fill="both", padx=150, ipady=20, pady=20)
        form_frame.pack(expand=True, fill="both", ipady=30)

        # create the button frame
        reset = ctk.CTkButton(
            buttons_frame,
            text="Reset",
            fg_color="red",
            command=lambda: self.reset_entries(entries),
        )
        load_csv = ctk.CTkButton(
            buttons_frame,
            text="Stream from csv",
            fg_color="green",
            command=self.read_dataframe,
        )
        stream = ctk.CTkButton(
            buttons_frame,
            text="Stream",
            fg_color="blue",
            command=lambda: self.stream_data(),
        )
        reset.grid(row=0, column=0)
        load_csv.grid(row=0, column=1)
        stream.grid(row=0, column=2)
        buttons_frame.pack(expand=True, fill="x", padx=150)

    def tab_changed(self):
        if self.tab.get() == "Pharmacy":
            self.dataset = "symptoms"
            self.create_pharmacy_frame()

        else:
            self.dataset = "heartdisease"
            self.create_hospital_frame()

        print("default dataset", self.dataset)

    def read_dataframe(self):
        self.dataframe = None
        path = askopenfilename()
        print(path)
        self.dataframe = pd.read_csv(path)
        self.stream_csv()
        print(self.dataframe.columns)

    def set_method(self, method="k-anonymity"):
        self.method = method
        print(self.method)

    def set_dataset(self, dataset="heartdisease"):
        self.dataset = dataset
        self.create_hospital_frame()
        print("current dataset :", dataset)

    def stream_data(self):
        global producer
        data = {}
        if self.dataset == "symptoms":
            print(pharmacy_entries)
            for key, value in pharmacy_entries.items():
                data[key] = value.get()
                print(key, value.get())
        else:
            print(hospital_entries[self.dataset])
            for key, value in hospital_entries[self.dataset].items():
                data[key] = value.get()
                print(key, value.get())
        future = producer.send(self.dataset, privacy(data, []))
        future.get(timeout=30)

    def stream_csv(self):
        streamed_df = dict(self.dataframe)
        for key,value in streamed_df.items():
            streamed_df[key] = list(value)
        future = producer.send(self.dataset, privacy(streamed_df, []))
        future.get(timeout=30)


App()
