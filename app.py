import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageFont
import io

def initialize_data():
    if 'packing_list' not in st.session_state:
        st.session_state.packing_list = {
            "[공통] 공연장 휴대용 배낭": {
                "[배면 포켓]": ["선크림", "모기 퇴치 스프레이"],
                "[사이드 포켓]": ["물병/텀블러"],
                "[배낭]": ["수건", "판초 우의", "바람막이", "물티슈", "쿨링티슈", "이어플러그", "휴대폰 방수팩", "맥주 너클 오프너"],
                "<노란 파우치>": ["보조배터리", "USB 케이블류", "헤드랜턴", "AAA 건전지", "지퍼백"],
                "<빨간 파우치>": ["스포츠 테이핑 테이프", "대일밴드 (반창고)", "손톱깎이", "콘택트렌즈", "휴대용 티슈", "벌레 물린 약", "립밤", "상처 연고", "방수테이프"]
            },
            "[공통] 당일 챙길 것": {
                "<여권/결제>": ["여권", "항공권", "여행자보험", "일본 교통카드", "eSIM", "엔화 현금"],
                "<카드 지갑>": ["운전면허증", "신용카드"],
                "<티켓/기타>": ["주차권", "손목밴드 (입장권)", "후지락앱", "손수건", "차 열쇠", "애플워치", "애플워치 충전기/배터리", "멀티탭", "스킨/토너 (여행용)", "크림 (여행용)", "면도기 (여분)", "무선 이어폰", "카메라", "메모리카드"]
            },
            "[공통] 당일 착용할 것": {
                "": ["선글라스", "모자", "기능성 이너웨어", "기능성 상의", "기능성 하의", "T셔츠", "속건성 바지", "속옷", "손수건", "스마트폰"]
            },
            "[숙소 이용자용] 캐리어": {
                "[등 포켓]": ["지갑 (카드류 제외)"],
                "[내용물]": ["캐리어", "보조가방", "장바구니", "비닐봉지", "페스티벌용 T셔츠 (3장)", "속옷 (1장)", "양말 (1켤레)", "여분 수건", "3일차 손수건", "헤어 스프레이", "스킨/토너", "크림", "면도기", "슬리퍼", "머리끈"],
                "[충전/가전]": ["멀티플러그 (돼지코)", "충전 어댑터"],
                "[위생/세안]": ["샴푸", "바디워시", "세안제", "치약", "칫솔", "빗", "토너패드", "클렌징 패드", "마스크팩"],
                "[의약품]": ["감기약", "해열·진통제", "소화제", "변비약", "지사제"],
                "[빨래 용품]": ["세탁세제", "세탁망", "접이식 옷걸이"]
            },
            "[캠핑/차박용] 야영 및 차량 보관": {
                "": ["에어매트", "미니 아이스박스", "접이식 우산", "돗자리", "손선풍기"],
                "[차박 박스]": ["바디 시트", "취침용 T셔츠", "속옷 (2장)", "양말 (1켤레)", "복귀용 여분 옷", "비닐봉지 (여분)", "2일차 수건", "3일차 수건", "막 쓰는 수건", "2일차 손수건 (빨아서 쓰기)", "모자 (캡)", "이어플러그"],
                "[기타 박스]": ["장화", "샌들", "차량용 햇빛 가리개", "주방세제", "수세미", "일회용 장갑", "네임펜"],
                "[노란 배낭]": ["접이식 의자 (대)"]
            }
        }
    
    if 'checked_items' not in st.session_state:
        st.session_state.checked_items = set()
    else:
        # Filter out items that are no longer in the checklist to prevent progress calculation errors
        all_items = set()
        for category_data in st.session_state.packing_list.values():
            for items in category_data.values():
                all_items.update(items)
        st.session_state.checked_items = {item for item in st.session_state.checked_items if item in all_items}

def reset_checklist():
    st.session_state.checked_items.clear()
    for category, category_data in st.session_state.packing_list.items():
        for subheader, items in category_data.items():
            for item in items:
                if item in st.session_state:
                    st.session_state[item] = False

def generate_checklist_image():
    # Setup dimensions dynamically based on actual list sizes and subheaders to prevent clipping
    width = 800
    
    total_items = sum(len(items) for category_data in st.session_state.packing_list.values() for items in category_data.values())
    num_categories = len(st.session_state.packing_list)
    num_subheaders = sum(1 for category_data in st.session_state.packing_list.values() for subheader in category_data.keys() if subheader)
    
    # 250 (header space) + (items * 35) + (subheaders * 35) + (categories * 65) + 100 (footer padding)
    height = 250 + (total_items * 35) + (num_subheaders * 35) + (num_categories * 65) + 100
    
    # Create image with premium dark background
    image = Image.new("RGB", (width, height), "#1A1A24")
    draw = ImageDraw.Draw(image)
    
    # Load fonts
    font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    try:
        font_title = ImageFont.truetype(font_path, 36)
        font_subtitle = ImageFont.truetype(font_path, 20)
        font_category = ImageFont.truetype(font_path, 26)
        font_item = ImageFont.truetype(font_path, 22)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_category = ImageFont.load_default()
        font_item = ImageFont.load_default()
        
    # Draw header (No emojis to prevent tofu boxes)
    draw.text((width/2, 60), "FUJI ROCK FESTIVAL", fill="#FF8A00", font=font_title, anchor="ms")
    draw.text((width/2, 100), "CHECKLIST", fill="#FFFFFF", font=font_subtitle, anchor="ms")
    
    # Calculate progress
    progress_pct = int((checked_count / total_items) * 100) if total_items > 0 else 0
    
    # Draw progress bar container
    pb_x = 80
    pb_y = 130
    pb_w = width - 160
    pb_h = 24
    draw.rounded_rectangle([pb_x, pb_y, pb_x + pb_w, pb_y + pb_h], radius=12, fill="#2D2D3D")
    
    # Draw filled progress bar
    if checked_count > 0:
        filled_w = (pb_w * checked_count) // total_items
        draw.rounded_rectangle([pb_x, pb_y, pb_x + filled_w, pb_y + pb_h], radius=12, fill="#FF4B4B")
        
    # Draw progress text
    progress_text = f"선택 항목: {progress_pct}% ({checked_count} / {total_items})"
    draw.text((width/2, 185), progress_text, fill="#A0A0B0", font=font_subtitle, anchor="ms")
    
    # Draw divider line
    draw.line([60, 210, width - 60, 210], fill="#3D3D4D", width=2)
    
    # Draw list categories, subheaders and items
    curr_y = 250
    x_left = 80
    
    for category, category_data in st.session_state.packing_list.items():
        # Category header
        draw.text((x_left, curr_y), category, fill="#FF8A00", font=font_category)
        curr_y += 45
        
        for subheader, items in category_data.items():
            if subheader:
                # Draw subheader
                draw.text((x_left + 10, curr_y), f"— {subheader}", fill="#FF4B4B", font=font_subtitle)
                curr_y += 35
                
            for item in items:
                is_checked = item in st.session_state.checked_items
                box_size = 20
                box_x = x_left + 20 if subheader else x_left + 10
                box_y = curr_y + 4
                
                if is_checked:
                    # Draw filled red checkbox
                    draw.rounded_rectangle([box_x, box_y, box_x + box_size, box_y + box_size], radius=4, fill="#FF4B4B")
                    # Draw white checkmark
                    draw.line([box_x + 5, box_y + 10, box_x + 9, box_y + 14], fill="#FFFFFF", width=2)
                    draw.line([box_x + 9, box_y + 14, box_x + 15, box_y + 6], fill="#FFFFFF", width=2)
                else:
                    # Draw empty checkbox
                    draw.rounded_rectangle([box_x, box_y, box_x + box_size, box_y + box_size], radius=4, outline="#A0A0B0", width=2)
                
                # Draw text (without drag handle characters in exported image)
                text_x = box_x + box_size + 20
                text_color = "#FFFFFF" if not is_checked else "#A0A0B0"
                draw.text((text_x, curr_y), item, fill=text_color, font=font_item)
                curr_y += 35
                
        curr_y += 20
        
    # Draw footer
    draw.text((width/2, height - 40), "만든이 @sigong © 2026 | Inspired by c86tori | v1.4.0", fill="#505060", font=font_subtitle, anchor="ms")
    
    # Save image to buffer and return bytes
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=95)
    return buf.getvalue()

def main():
    st.set_page_config(page_title="후지록 준비물 체크리스트", layout="centered")
    
    # Sidebar User Guide
    with st.sidebar:
        st.title("ℹ️ 후지록 체크리스트 가이드")
        st.markdown("""
        ### 💡 기본 기능
        * **체크리스트 관리:** 준비물을 선택하면 진행률 상태링과 진행률 백분율이 실시간 업데이트됩니다.
        * **자동 저장:** 체크 상태, 정렬 상태, 배너 등 모든 변경사항은 브라우저에 즉시 안전하게 자동 저장됩니다.
        
        ### ✏️ 편집 모드 (커스터마이징)
        * **항목 위치 변경:** `✏️ 편집 모드`를 누르고 좌측 손잡이(⠿)나 항목 자체를 마우스/손가락으로 드래그하여 순서를 마음대로 바꿀 수 있습니다.
        * **나만의 배너 업로드:** 편집 모드 상태에서 상단 배너 영역의 `📷 배너 이미지 변경` 단추를 누르면 원하는 사진으로 커스텀 배너를 지정할 수 있습니다.
        
        ### 📸 이미지 내보내기 & 리셋
        * **이미지로 저장 (JPG):** `📸 이미지로 저장` 단추를 누르면 내가 체크한 항목과 진행률(선택 항목 비율)이 담긴 고해상도 JPG 이미지 카드를 다운로드할 수 있어, 오프라인이나 락페 현장에서 사진첩으로 빠르게 볼 수 있습니다.
        * **초기화:** 리스트 상태를 완전히 처음 기본값으로 되돌리고 싶을 때 사용합니다.
        """)
        
        # Collapsible Changelog expander
        with st.expander("🆕 업데이트 내역 (Changelog)"):
            try:
                with open("CHANGELOG.md", "r", encoding="utf-8") as f:
                    changelog_content = f.read()
                # Remove header lines for cleaner sidebar rendering
                if "---" in changelog_content:
                    changelog_content = changelog_content.split("---", 1)[1].strip()
                st.markdown(changelog_content)
            except Exception:
                st.write("업데이트 내역을 불러올 수 없습니다.")
    
    # Inject JavaScript to localize the Streamlit menu and settings modal into Korean, and hide Development options
    components.html("""
    <script>
    const parentDoc = window.parent.document;
    const translations = {
        "Rerun": "다시 실행",
        "Settings": "설정",
        "Print": "인쇄",
        "Record a screencast": "화면 녹화",
        "Developer options": "개발자 옵션",
        "Clear cache": "캐시 지우기",
        "Development": "개발 설정",
        "Run on save": "저장 시 자동 실행",
        "Automatically updates the app when the underlying code is updated.": "코드가 변경되면 앱을 자동으로 업데이트합니다.",
        "Appearance": "화면 구성",
        "Wide mode": "와이드 모드",
        "Turn on to make this app occupy the entire width of the screen.": "화면 전체 너비를 차지하도록 설정합니다.",
        "Choose app theme, colors and fonts": "앱 테마, 색상 및 글꼴 선택",
        "Use system setting": "시스템 설정 사용",
        "Light": "라이트 모드",
        "Dark": "다크 모드",
        "Custom": "사용자 지정",
        "Edit active theme": "현재 테마 편집",
        "Made with Streamlit": "Streamlit으로 제작됨"
    };

    function translateText(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.nodeValue.trim();
            for (const [key, value] of Object.entries(translations)) {
                if (text.includes(key)) {
                    node.nodeValue = node.nodeValue.replace(key, value);
                }
            }
        } else {
            for (const child of node.childNodes) {
                translateText(child);
            }
        }
    }

    function cleanDevelopmentSection(root) {
        if (!root || typeof root.querySelectorAll !== 'function') return;
        const allElements = root.querySelectorAll('*');
        allElements.forEach(el => {
            if (el.children.length === 0 || Array.from(el.childNodes).some(c => c.nodeType === Node.TEXT_NODE && c.nodeValue.trim())) {
                const text = el.textContent.trim();
                if (text === "Development" || text === "개발 설정" || 
                    text === "Run on save" || text === "저장 시 자동 실행" || 
                    text.includes("Automatically updates the app") || text.includes("코드가 변경되면 앱을 자동으로")) {
                    
                    let container = el.closest('[data-testid="stCheckbox"]') || el.closest('label');
                    if (container) {
                        container.style.setProperty('display', 'none', 'important');
                    } else {
                        let block = el.closest('h1, h2, h3, h4, p, [class*="StyledCaptionContainer"], [data-testid="stText"]');
                        if (block) {
                            block.style.setProperty('display', 'none', 'important');
                        } else {
                            el.style.setProperty('display', 'none', 'important');
                        }
                    }
                }
            }
        });
    }

    // Observe updates in the parent DOM to translate popups/modals and hide development options when they open
    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            for (const node of mutation.addedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    translateText(node);
                    cleanDevelopmentSection(node);
                }
            }
        }
    });

    observer.observe(parentDoc.body, { childList: true, subtree: true });
    translateText(parentDoc.body);
    cleanDevelopmentSection(parentDoc.body);
    </script>
    """, height=0, width=0)

    st.title("후지록 페스티벌 준비물 리스트")
    st.write("체크박스를 눌러 준비 상태를 확인하세요.")

    initialize_data()

    # Sync checked_items with widget states first to prevent rendering lag
    for category, category_data in st.session_state.packing_list.items():
        for subheader, items in category_data.items():
            for item in items:
                if item in st.session_state:
                    if st.session_state[item]:
                        st.session_state.checked_items.add(item)
                    else:
                        st.session_state.checked_items.discard(item)

    global checked_count, total_items
    total_items = sum(len(items) for category_data in st.session_state.packing_list.values() for items in category_data.values())
    checked_count = len(st.session_state.checked_items)
    
    st.progress(checked_count / total_items if total_items > 0 else 0)
    
    st.markdown(
        "<div style='text-align: center; color: #a0a0b0; font-size: 0.95rem; margin-top: -10px; margin-bottom: 15px;'>"
        "⠿ 마우스로 드래그 하여 항목 위치 변경 가능, 탭으로 확인"
        "</div>", 
        unsafe_allow_html=True
    )
    
    # Progress info, download button, and reset button row (Top)
    col_status, col_download, col_reset = st.columns([1.5, 1, 1])
    with col_status:
        st.write(f"📊 **진행률: {checked_count} / {total_items}**")
    with col_download:
        img_data = generate_checklist_image()
        st.download_button(
            label="📸 이미지로 저장",
            data=img_data,
            file_name="fujirock_checklist.jpg",
            mime="image/jpeg",
            key="download_btn_top"
        )
    with col_reset:
        st.button("🔄 초기화", on_click=reset_checklist, key="reset_btn_top")

    for category, category_data in st.session_state.packing_list.items():
        # Calculate category statistics
        cat_total = sum(len(items) for items in category_data.values())
        cat_checked = sum(1 for items in category_data.values() for item in items if item in st.session_state.checked_items)
        
        # Expander with live progress label and visual drag handle prefix
        expander_title = f"⠿ {category} ({cat_checked} / {cat_total})"
        
        with st.expander(expander_title, expanded=False):
            for subheader, items in category_data.items():
                if subheader:
                    st.markdown(f"**⠿ — {subheader}**")
                for item in items:
                    is_checked = item in st.session_state.checked_items
                    label = f"⠿ ↳ {item}" if subheader else f"⠿ {item}"
                    changed = st.checkbox(label, value=is_checked, key=item)
                    
                    if changed and not is_checked:
                        st.session_state.checked_items.add(item)
                    elif not changed and is_checked:
                        st.session_state.checked_items.remove(item)

    # Progress info, download button, and reset button row (Bottom)
    st.write("---")
    col_status_b, col_download_b, col_reset_b = st.columns([1.5, 1, 1])
    with col_status_b:
        st.write(f"📊 **진행률: {checked_count} / {total_items}**")
    with col_download_b:
        img_data = generate_checklist_image()
        st.download_button(
            label="📸 이미지로 저장",
            data=img_data,
            file_name="fujirock_checklist.jpg",
            mime="image/jpeg",
            key="download_btn_bottom"
        )
    with col_reset_b:
        st.button("🔄 초기화", on_click=reset_checklist, key="reset_btn_bottom")

    # Footer
    st.markdown("<p style='text-align: center; color: #a0a0b0; margin-top: 50px; display: flex; align-items: center; justify-content: center; gap: 4px;'>만든이 <a href='https://www.instagram.com/sigong' target='_blank' rel='noopener noreferrer' style='color: #FF5B5B; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;'><svg viewBox='0 0 24 24' width='16' height='16' fill='currentColor' style='display: inline-block; vertical-align: middle;'><path d='M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z'/></svg>@sigong</a> &copy; 2026 | Inspired by c86tori | v1.4.0</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
