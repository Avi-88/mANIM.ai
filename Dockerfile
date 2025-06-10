FROM manimcommunity/manim:stable

USER root

# Install LaTeX
RUN apt-get update && \
    apt-get install -y texlive-full && \
    apt-get install -y xdg-utils && \
    apt-get clean