import glob
import csv
from paddleocr import PaddleOCR
import numpy as np
import matplotlib.pyplot as plt

def process_pdf(pdf_file, ocr_engine):
    result = ocr_engine.ocr(pdf_file, cls=False)
    accuracies = []
    for page, line_data in enumerate(result):
        for line in line_data:
            confidence = line[1][1]
            accuracies.append(confidence)
    return np.mean(accuracies)


def plot_accuracy_distribution(csv_file):
    accuracies = []

    with open(csv_file, "r", encoding="utf-8", newline='') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header

        for row in csv_reader:
            accuracy = float(row[1])
            accuracies.append(accuracy)

    num_files = len(accuracies)

    # Plotting the distribution
    plt.hist(accuracies, bins=10, density=True, alpha=0.6, color='b')
    plt.xlabel('Accuracy (%)')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of OCR Accuracies (n={num_files})')

    # Plotting the percentage curve
    sorted_accuracies = np.sort(accuracies)
    yvals = np.arange(len(sorted_accuracies)) / float(len(sorted_accuracies))
    plt.plot(sorted_accuracies, yvals, color='r', label='Percentage Curve')
    plt.legend(loc='upper left')

    plt.savefig('accuracy_test_plot.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    ocr_engine = PaddleOCR(lang="en", cpu_threads=8, use_mp=True)
    pdf_files = glob.glob("test_examples/*.pdf")
    output_file = "results.csv"

    with open(output_file, "w", encoding="utf-8", newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["File", "Accuracy"])

        for pdf_file in pdf_files:
            avg_accuracy = process_pdf(pdf_file, ocr_engine)
            avg_accuracy_percentage = avg_accuracy * 100
            csv_writer.writerow([pdf_file, f"{avg_accuracy_percentage:.2f}"])
            print(f"Processed {pdf_file} with average accuracy {avg_accuracy_percentage:.2f}%")




if __name__ == "__main__":
    main()
    plot_accuracy_distribution('results.csv')
