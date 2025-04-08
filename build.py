import fitz
import os

def merge_pdfs(pdf_below_path, pdf_above_path, output_path):
    pdf_below = fitz.open(pdf_below_path)
    pdf_above = fitz.open(pdf_above_path)

    if not pdf_below.page_count == 1 and not pdf_above.page_count == 1:
        raise ValueError("Both PDFs must contain exactly one page.")

    page_below = pdf_below.load_page(0)
    page_above = pdf_above.load_page(0)

    rect_below = page_below.rect
    rect_above = page_above.rect

    if rect_below != rect_above:
        raise ValueError("Both PDFs must have the same page size.")

    pdf_output = fitz.open()
    merged_page = pdf_output.new_page(width=rect_below.width, height=rect_below.height)

    merged_page.show_pdf_page(rect_below, pdf_below, 0)

    # Overlay the PDF page
    merged_page.show_pdf_page(rect_below, pdf_above, 0)

    pdf_output.set_metadata(pdf_below.metadata)
    pdf_output.save(output_path)

    pdf_output.close()
    pdf_below.close()
    pdf_above.close()

def main():
    pdf_below_path = "SD_Standard_BY-NC-SA.pdf"
    pdf_above_path = "SD_Standard_BY-SA.pdf"
    output_path = "SD_Standard.pdf"

    if not os.path.exists(pdf_below_path):
        raise FileNotFoundError(f"{pdf_below_path} does not exist. See README.md for instructions.")
    if not os.path.exists(pdf_above_path):
        raise FileNotFoundError(f"{pdf_above_path} does not exist. See README.md for instructions.")

    if os.path.exists(output_path):
        confirm = input(f"{output_path} already exists. Overwrite? (y/N): ")
        if confirm.lower() == 'n' or confirm == '':
            print("Build canceled.")
            return
        elif confirm.lower() != 'y':
            print("Invalid input. Build canceled.")
            return

    merge_pdfs(pdf_below_path, pdf_above_path, output_path)

    print(f"Saved {output_path}")

if __name__ == "__main__":
    main()
