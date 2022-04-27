from flask import Flask, render_template, url_for, request, redirect, Blueprint, json, flash, session, make_response
from weasyprint import HTML, CSS

app = Flask(__name__)

@app.route("/")
def hello():
	name = "salman"
	age = 25
	page = render_template('page.html', name=name, age=age)
	html = HTML(string=page)
	pdf = html.write_pdf(stylesheets=[CSS('static/css/style.css')])
	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
	return response
	# return render_template('home.html')

@app.route("/full")
def full():
	# Main template
	name = "salman"
	age = 25
	page = render_template('page.html', name=name, age=age)
	html = HTML(string=page)
	main_doc = html.render(stylesheets=[CSS('static/css/style.css')])

	exists_links = False

	# Template of header
	header_html = render_template('header.html')
	html = HTML(string=header_html)
	# header = html.render(stylesheets=[CSS('static/css/style.css')])
	header = html.render()

	header_page = header.pages[0]
	exists_links = exists_links or header_page.links
	header_body = get_page_body(header_page._page_box.all_children())
	header_body = header_body.copy_with_children(header_body.all_children())

	# Template of footer
	footer_html = render_template('footer.html')
	html = HTML(string=footer_html)
	# footer = html.render(stylesheets=[CSS('static/css/style.css')])
	footer = html.render()

	footer_page = footer.pages[0]
	exists_links = exists_links or footer_page.links
	footer_body = get_page_body(footer_page._page_box.all_children())
	footer_body = footer_body.copy_with_children(footer_body.all_children())


	# Insert header and footer in main doc
	for i, page in enumerate(main_doc.pages):
		# if not i:
		# 	continue

		page_body = get_page_body(page._page_box.all_children())

		page_body.children += header_body.all_children()
		page_body.children += footer_body.all_children()

		if exists_links:
			page.links.extend(header_page.links)
			page.links.extend(footer_page.links)

	pdf = main_doc.write_pdf()
	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
	return response


def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == 'body':
            return box

        return get_page_body(box.all_children())

if __name__ == "__main__":
    app.run(debug=True)