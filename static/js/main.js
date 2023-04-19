  gsap.registerPlugin(ScrollTrigger);

  const marqueeAnimation = () => {
    const marqueeText = document.querySelector(".marquee-text");
    gsap.fromTo(
      marqueeText,
      { x: "100%" },
      {
        x: "-60%",
        duration: 10,
        scrollTrigger: {
          trigger: document.body,
          start: "top top",
          end: "bottom bottom",
          scrub: true,
        },
      }
    );
  };

  gsap.to(".animate", {
    opacity: 1,
    y: 0,
    duration: 1,
    ease: "power1.out",
    scrollTrigger: {
      trigger: ".animation",
      start: "top 80%",
      end: "bottom 30%",
      toggleActions: "play none none reverse"
    }
  });

  marqueeAnimation();


