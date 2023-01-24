from flet import *
import sqlite3
import base64
import os

# CONNECT TO YOU DATABASE FILE SQLITE 
conn = sqlite3.connect("database.db",check_same_thread=False)
cursor = conn.cursor()


def main(page:Page):
	page.scroll = "auto"
	youdata = Column()
	txtname = TextField(label="you name here")


	def uploadnow(e:FilePickerResultEvent):
		# IF THERE FILE 
		if not e.files == "":
			for x in e.files:
				try:
					with open(x.path,"rb") as image_file:
						convertImgToString = base64.b64encode(image_file.read()).decode()
						# THEN INSERT TO TABLE 
						cursor.execute("INSERT INTO images (name,gambar) VALUES (?,?) ",(txtname.value,convertImgToString))
						conn.commit()
						print("You SUccess uploading file guys !!!!!")
						page.update()
				except Exception as e:
					print(e)
					print("YOU HAVE PROBLEM HERE !!!!")
				page.update()


	# AFTER THAT , I WANT LOAD DATA WHEN APP ONECE LOADED
	# LIKE LIFECYCLE 
	cursor.execute("select * from images")
	data = cursor.fetchall()

	sample = []
	# IF DATA FOUND FROM YOU TABLE SQLITE THEN PUSH TO COLUMN WIDGET
	if not len(data) == 0:
		for x in data :
			sample.append({"id":x[0],"nama":x[1],"gambar":x[2]})
			for p in sample:
				youdata.controls.append(
					Container(
					content=Column([
						Text(f"{p['nama']}",size=30),
						Image(
						src_base64=p['gambar'],
						width=300,
						height=200,
						fit="cover"

							)

						])

						)

					)



	file_picker = FilePicker(
		on_result=uploadnow

		)
	page.overlay.append(file_picker)
	page.add(
		Column([
		Text("SQLITE UPLOAD IMAGE BLOB",size=30),
		txtname,
		FilledButton("upload now ",
		on_click=lambda e:file_picker.pick_files()
		),
		youdata 


			])
		)


flet.app(target=main)
