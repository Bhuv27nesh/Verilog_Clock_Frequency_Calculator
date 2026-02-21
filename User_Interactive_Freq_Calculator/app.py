from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_delay(time_unit, freq, unit_type):
    # Convert frequency to Hz
    if unit_type == "kHz":
        freq_hz = float(freq) * 1e3
    elif unit_type == "MHz":
        freq_hz = float(freq) * 1e6
    elif unit_type == "GHz":
        freq_hz = float(freq) * 1e9
    else:
        freq_hz = float(freq)

    # Convert time unit to seconds
    unit_map = {
        "1ns": 1e-9,
        "1ps": 1e-12,
        "1us": 1e-6
    }

    time_in_sec = unit_map[time_unit]

    # Half period
    delay = 1 / (2 * freq_hz * time_in_sec)

    return round(delay, 6)


@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    if request.method == "POST":
        time_unit = request.form["time_unit"]
        time_precision = request.form["time_precision"]
        freq = request.form["frequency"]
        unit_type = request.form["freq_unit"]
        block_type = request.form["block_type"]

        delay = calculate_delay(time_unit, freq, unit_type)

        if block_type == "always":
            code = f"""`timescale {time_unit}/{time_precision}

reg clk = 0;
always #{delay} clk = ~clk;"""

        elif block_type == "repeat":
            code = f"""`timescale {time_unit}/{time_precision}

reg clk = 0;
initial begin
  repeat(100)
    #{delay} clk = ~clk;
end"""

        elif block_type == "for":
            code = f"""`timescale {time_unit}/{time_precision}

reg clk = 0;
integer i;
initial begin
  for(i=0;i<100;i=i+1)
    #{delay} clk = ~clk;
end"""

        elif block_type == "while":
            code = f"""`timescale {time_unit}/{time_precision}

reg clk = 0;
initial begin
  while(1)
    #{delay} clk = ~clk;
end"""

    return render_template("index.html", code=code)


if __name__ == "__main__":
    app.run(debug=True)
