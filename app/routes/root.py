from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.models.contact import ContactRequest

from app.utils.email import send_email

root_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@root_router.get("/contact", response_class=HTMLResponse)
async def contact_form(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@root_router.post("/contact", response_class=HTMLResponse)
async def handle_contact(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    description: str = Form(...),
    subject: str = Form("Contact Request")
):
    try:
        # Create contact request
        contact_data = ContactRequest(
            first_name=first_name,
            last_name=last_name,
            email=email,
            description=description,
            subject=subject
        )

        # Format email content
        email_body = f"""
        New contact request:

        Name: {contact_data.first_name} {contact_data.last_name}
        Email: {contact_data.email}
        Subject: {contact_data.subject}
        Message: {contact_data.description}
        """

        # Send email to admin
        success = send_email(
            to_email="raedrdhaounia@gmail.com",
            subject=f"New Contact Request: {contact_data.subject}",
            body=email_body
        )

        # Send confirmation email to user
        user_success = send_email(
            to_email=contact_data.email,
            subject="Thank you for contacting us",
            body="Thank you for your message. We will get back to you soon."
        )

        if success and user_success:
            return templates.TemplateResponse(
                "contact.html",
                {"request": request, "message": "Message sent successfully!"}
            )
        else:
            return templates.TemplateResponse(
                "contact.html",
                {"request": request, "message": "Failed to send message. Please try again later."}
            )

    except Exception as e:
        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "message": f"An error occurred: {str(e)}"}
        )

@root_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@root_router.get("/terms")
async def terms(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})

@root_router.get("/privacy")
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})