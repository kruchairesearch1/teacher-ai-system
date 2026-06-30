from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime

app = FastAPI()

# เปิดการเชื่อมต่อให้หน้าเว็บ (HTML) เรียกใช้ Python ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ฐานข้อมูลวิชาเรียน
subject_data = {
    "คณิตศาสตร์": {"detail": "กระบวนการคิดวิเคราะห์เชิงตัวเลข และการแก้ปัญหาอย่างเป็นระบบ", "advice": "เน้นการสร้างสถานการณ์ปัญหาที่สัมพันธ์กับชีวิตจริง"},
    "ภาษาไทย": {"detail": "ทักษะการอ่าน เขียน และการสื่อสารอย่างสร้างสรรค์", "advice": "มุ่งเน้นการวิเคราะห์วรรณศิลป์และการนำเสนอผลงานด้วยตนเอง"},
    "วิทยาศาสตร์และเทคโนโลยี": {"detail": "การสืบเสาะหาความรู้และกระบวนการทางวิทยาศาสตร์", "advice": "ส่งเสริมการตั้งสมมติฐานและการทดลองเชิงประจักษ์"},
    "สังคมศึกษา ศาสนา และวัฒนธรรม": {"detail": "การเชื่อมโยงเหตุการณ์ประวัติศาสตร์และบริบททางสังคม", "advice": "ใช้กระบวนการอภิปรายกลุ่มเพื่อให้เข้าใจมุมมองที่หลากหลาย"},
    "ภาษาต่างประเทศ": {"detail": "ทักษะการฟัง พูด อ่าน และเขียนเพื่อการสื่อสาร", "advice": "เน้นสร้างสถานการณ์จำลองเพื่อให้ผู้เรียนใช้ภาษาในบริบทจริง"},
    "ศิลปะ": {"detail": "การแสดงออกทางอารมณ์ และความคิดสร้างสรรค์", "advice": "เปิดโอกาสให้ผู้เรียนวิพากษ์งานศิลปะเพื่อสร้างความเข้าใจในคุณค่า"},
    "สุขศึกษาและพลศึกษา": {"detail": "การสร้างสุขภาวะทางกาย จิต และทักษะการทำงานเป็นทีม", "advice": "เน้นการประยุกต์ใช้ในการดูแลสุขภาพที่ยั่งยืน"},
    "การงานอาชีพ": {"detail": "ทักษะการปฏิบัติงานจริง และการใช้นวัตกรรมในการแก้ปัญหา", "advice": "ให้ความสำคัญกับการฝึกฝนผ่านกิจกรรมที่ประณีตและสร้างสรรค์"},
    "วิทยาการคำนวณ": {"detail": "ทักษะการคิดเชิงคำนวณ (Computational Thinking) และตรรกะ", "advice": "เน้นการแก้ปัญหาผ่านโครงงานดิจิทัลที่สร้างสรรค์"},
    "ประวัติศาสตร์": {"detail": "การเชื่อมโยงเหตุการณ์ในอดีตกับสถานการณ์ปัจจุบัน", "advice": "ควรใช้สื่อมัลติมีเดียที่ทำให้ประวัติศาสตร์น่าสนใจ"}
}

class SessionData(BaseModel):
    subject: str
    level: str
    topic: str
    engagement_data: list

@app.post("/analyze")
async def analyze_data(data: SessionData):
    # คำนวณค่าเฉลี่ยความสนใจ
    avg = sum(data.engagement_data) / len(data.engagement_data) if data.engagement_data else 0
    status = "ดีเยี่ยม" if avg > 75 else "ควรปรับปรุง"
    subj_info = subject_data.get(data.subject, {"detail": "การเรียนรู้เชิงรุก", "advice": "รักษาบรรยากาศการเรียนรู้ที่ดี"})
    
    # รูปแบบรายงานที่คุณต้องการ
    report_content = f"""
    <div class="p-8 bg-white text-black border border-gray-400 rounded-lg shadow-sm">
        <h1 class="text-center font-bold text-2xl mb-8">บันทึกรายงานการประเมินการจัดการเรียนรู้</h1>
        <div class="grid grid-cols-2 gap-4 mb-8 border-b border-gray-300 pb-6">
            <p><strong>วิชา:</strong> {data.subject}</p><p><strong>ระดับชั้น:</strong> {data.level}</p>
            <p><strong>เรื่อง:</strong> {data.topic}</p><p><strong>วันที่:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
        </div>
        <h3 class="font-bold text-lg mb-2 underline">1. สรุปภาพรวม</h3>
        <p class="mb-6">การมีส่วนร่วมของผู้เรียนโดยเฉลี่ยอยู่ที่ <strong>{avg:.2f}%</strong> ซึ่งอยู่ในเกณฑ์ <strong>{status}</strong></p>
        <h3 class="font-bold text-lg mb-2 underline">2. วิเคราะห์พฤติกรรม</h3>
        <p class="mb-6">{subj_info['detail']}</p>
        <h3 class="font-bold text-lg mb-2 underline">3. ข้อเสนอแนะเชิงพัฒนา</h3>
        <p class="mb-16">{subj_info['advice']} อีกทั้งควรส่งเสริมให้ผู้เรียนสรุปองค์ความรู้ด้วยตนเอง เพื่อให้เกิดทักษะการเรียนรู้ที่ยั่งยืน</p>
        <div class="flex justify-between mt-12">
            <div class="text-center w-1/2">ลงชื่อ......................................<br>(..................................................)<br>ผู้รับการประเมิน</div>
            <div class="text-center w-1/2">ลงชื่อ......................................<br>(..................................................)<br>ผู้บริหารสถานศึกษา</div>
        </div>
    </div>
    """
    return {"content": report_content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)