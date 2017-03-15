import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Run a model simulation")
    parser.add_argument("--model_name")
    parser.add_argument("--file_dir")
    parser.add_argument("--file_name")
    parser.add_argument("--save_path")
    parser.add_argument("--CPU", type=int)
    parser.add_argument("--parameters", nargs="*")
    parser.add_argument("--model_kwargs", nargs="*")

    args = parser.parse_args()

    sys.path.insert(0, args.file_dir)
    module = __import__(args.file_name.split(".")[0])
    model = getattr(module, args.model_name)

    model_kwargs = dict(zip(args.model_kwargs[::2], args.model_kwargs[1::2]))
    simulation = model(**model_kwargs)

    if args.parameters is None:
        args.parameters = []

    parameters = {}
    i = 0
    while i < len(args.parameters):
        parameters[args.parameters[i]] = float(args.parameters[i+1])
        i += 2

    if len(args.parameters) % 2 != 0:
        msg = "Number of parameters does not match number of parametervalues sent to simulation"
        raise ValueError(msg)

    simulation.run(parameters)
    simulation.save(CPU=args.CPU, save_path=args.save_path)

if __name__ == "__main__":
    main()
