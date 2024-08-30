import streamlit as st
import videohelper
import raghelperr

if "current_video_url" not in st.session_state:
    st.session_state.current_video_url = None
    st.session_state.current_transcript_docs = []
    st.session_state.videos = []

st.set_page_config(page_title="VidChat: Chat with YouTube!", layout="centered")
st.image(image="./img/app_banner.png")
st.title("VidChat: Chat with YouTube! 🎥")
st.divider()

tab_url, tab_search = st.tabs(["Enter URL", "Search Video"])

with tab_url:
    video_url = st.text_input(label="Enter YouTube Video URL:", key="url_video_url")
    prompt = st.text_input(label="Enter Your Question:", key="url_prompt")
    submit_btn = st.button("Ask 🎤", key="url_submit")

    if submit_btn:
        st.video(data=video_url)
        st.divider()
        if st.session_state.current_video_url != video_url:
            with st.spinner("STEP 1: Preparing video transcript..."):
                video_transcript_docs = videohelper.get_video_transcript(url=video_url)
                st.session_state.current_transcript_docs = video_transcript_docs
        st.success("Video transcript cached successfully! 📄")
        st.divider()
        st.session_state.current_video_url = video_url

        with st.spinner("STEP 2: Answering your question..."):
            AI_Response, relevant_documents = raghelperr.rag_with_video_transcript(
                transcript_docs=st.session_state.current_transcript_docs, prompt=prompt)
        st.info("ANSWER:")
        st.markdown(AI_Response)
        st.divider()

        for doc in relevant_documents:
            st.warning("REFERENCE:")
            st.caption(doc.page_content)
            st.markdown(f"Source: {doc.metadata}")
            st.divider()

with tab_search:
    col_left, col_center, col_right = st.columns([20, 1, 10])

    with col_left:

        st.subheader("Video Search 🕵️‍♂️")
        st.divider()
        search_term = st.text_input(label="Enter Search Terms:", key="search_term")
        video_count = st.slider(label="Number of Results", min_value=1, max_value=5, value=5, key="search_video_count")
        sorting_options = ["relevance", "upload_date", "view_count", "rating"]
        sorting_criteria = st.selectbox(label="Sorting Criteria", options=sorting_options)
        search_btn = st.button(label="Search Video 🔍", key="search_button")
        st.divider()

        if search_btn:
            st.session_state.videos = []
            videolist = videohelper.get_videos_for_search_term(search_term=search_term, video_count=video_count,
                                                               sorting_criteria=sorting_criteria)

            for video in videolist:
                st.session_state.videos.append(video)

        video_urls = []
        video_titles = {}
        for video in st.session_state.videos:
            video_urls.append(video.video_url)
            video_titles.update({video.video_url: video.video_title})

        selected_video = st.selectbox(
            label="Select the Video to Chat With:",
            options=video_urls,
            format_func=lambda url: video_titles[url],
            key="search_selectbox"
        )

        if selected_video:
            search_prompt = st.text_input(label="Enter Your Question:", key="search_prompt")
            search_ask_btn = st.button(label="Ask 🎤", key="search_ask_button")

            if search_ask_btn:
                st.caption("Selected Video")
                st.video(data=selected_video)
                st.divider()

                if st.session_state.current_video_url != selected_video:
                    with st.spinner("STEP 1: Preparing video transcript..."):
                        video_transcript_docs = videohelper.get_video_transcript(url=selected_video)
                        st.session_state.current_transcript_docs = video_transcript_docs
                    st.success("Video transcript cached successfully! 📄")
                    st.divider()
                    st.session_state.current_video_url = selected_video

                with st.spinner("STEP 2: Answering your question..."):
                    AI_Response, relevant_documents = raghelperr.rag_with_video_transcript(
                        transcript_docs=st.session_state.current_transcript_docs, prompt=search_prompt)
                st.info("ANSWER:")
                st.markdown(AI_Response)
                st.divider()

                for doc in relevant_documents:
                    st.warning("REFERENCE:")
                    st.caption(doc.page_content)
                    st.markdown(f"Source: {doc.metadata}")
                    st.divider()

    with col_center:
        st.empty()

    with col_right:

        st.subheader("Related Videos 🎞️")
        st.divider()

        for i, video in enumerate(st.session_state.videos):
            st.info(f"Video No: {i + 1}")
            st.video(data=video.video_url)
            st.caption(f"Video Title: {video.video_title}")
            st.caption(f"Channel: {video.channel_name}")
            st.caption(f"Duration: {video.duration}")
            st.divider()
