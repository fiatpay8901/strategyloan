(function ($) {
    "use strict";
    $(window).on("scroll", function () {
        // header sticky
        if ($("header").length) {
            var headerScrollPos = 300;
            var stricky = $(".main-header");
            if ($(window).scrollTop() > headerScrollPos) {
                setTimeout(function () {
                    stricky.addClass("sticky-fixed");
                })
                stricky.addClass("sticky-header--cloned");
            } else if ($(this).scrollTop() <= headerScrollPos) {
                stricky.removeClass("sticky-fixed");
                stricky.removeClass("sticky-header--cloned");
            }
        }
    });
    if ($('.main-header').length) {
        // search popup
        $('.search-btn').on('click', function () {
            $('body').addClass('search-active');
        });
        $(' .close-search').on('click', function () {
            $('body').removeClass('search-active');
        });
    }
    if ($('.header-right-end').length) {
        // mobail nav
        $(".header-right-end").click(function () {
            $(".mobile-nav-wrapper").addClass("expanded");
        });
        $(".mobile-nav-toggler").click(function () {
            $(".mobile-nav-wrapper").removeClass("expanded");
        });
        $(".header-right-end").click(function () {
            $("body").addClass("locked");
        });
        $(".mobile-nav-toggler").click(function () {
            $("body").removeClass("locked");
        });

    }
    if ($('.header-side-menu').length) {
        // side menu
        $(".header-side-menu").click(function () {
            $(".side-menu-wrapper").addClass("expanded");
        });
        $(".side-menu-toggler").click(function () {
            $(".side-menu-wrapper").removeClass("expanded");
        });
        $(".header-side-menu").click(function () {
            $("body").addClass("locked");
        });
        $(".side-menu-toggler").click(function () {
            $("body").removeClass("locked");
        });

    }
    if ($(".mobile-nav-container .mobile-menu-list").length) {
        // mobaile nav bar 
        let dropdownAnchor = $(
            ".mobile-nav-container .mobile-menu-list .dropdown > a"
        );
        dropdownAnchor.each(function () {
            let self = $(this);
            let toggleBtn = document.createElement("BUTTON");
            toggleBtn.setAttribute("aria-label", "dropdown toggler");
            toggleBtn.innerHTML = "<i class='flaticon-right-arrow'></i>";
            self.append(function () {
                return toggleBtn;
            });
            self.find("button").on("click", function (e) {
                e.preventDefault();
                let self = $(this);
                self.toggleClass("expanded");
                self.parent().toggleClass("expanded");
                self.parent().parent().children("ul").slideToggle();
            });
        });
    }
    if ($('.banner-one').length) {
        // banner-one slider
        $('.banner-one-slider').slick({
            dots: true,
            infinite: true,
            speed: 200,
            autoplay: true,
            autoplaySpeed: 6000,
            slidesToShow: 1,
            fade: true,
            arrows: false,
            slidesToScroll: 1
        })
    }
    if ($('.banner-two').length) {
        const $slider = $('.banner-two-slider');
        // banner-one slider
        $('.banner-two-slider').slick({
            dots: true,
            infinite: true,
            speed: 200,
            autoplay: true,
            autoplaySpeed: 6000,
            slidesToShow: 1,
            fade: true,
            arrows: false,
            slidesToScroll: 1
        })
        // Custom dot creation
        const $dotsContainer = $('.slick-dots');
        $dotsContainer.empty();
        $slider.find('.banner-two-slider-item').each(function (index) {
            const text = $(this).data('dot');
            const isActive = index === 0 ? 'slick-active' : '';
            const dot = `<li class="${isActive}"><button type="button" data-slide="${index}"><span class="dot-text">${text}</span></button></li>`;
            $dotsContainer.append(dot);
        });
        $dotsContainer.on('click', 'button', function () {
            const slideIndex = $(this).data('slide');
            $slider.slick('slickGoTo', slideIndex);
        });
        $slider.on('afterChange', function (event, slick, currentSlide) {
            $('.banner-two .slick-dots li').removeClass('slick-active');
            $('.banner-two .slick-dots li').eq(currentSlide).addClass('slick-active');
        });
    }

    if ($('.partner-one').length) {
        // partner-one slider
        $('.partner-slider-one').slick({
            speed: 9000,
            autoplay: true,
            autoplaySpeed: 0,
            cssEase: 'linear',
            slidesToShow: 6,
            slidesToScroll: 1,
            dots: false,
            arrows: false,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 5,
                        slidesToScroll: 1,
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                    }
                }
            ]
        })
    }
    if ($('.partner-slider-two').length) {
        // partner-one slider
        $('.partner-slider-two').slick({
            speed: 5000,
            autoplay: true,
            autoplaySpeed: 0,
            cssEase: 'linear',
            slidesToShow: 5,
            slidesToScroll: 1,
            dots: false,
            arrows: false,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 4,
                        slidesToScroll: 1,
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                    }
                }
            ]
        })
    }
    if ($('.features-two').length) {
        // features-two slider
        $('.features-slider-two').slick({
            speed: 8000,
            autoplay: true,
            autoplaySpeed: 0,
            cssEase: 'linear',
            slidesToShow: 6,
            slidesToScroll: 1,
            variableWidth: true,
            dots: false,
            arrows: false,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 4,
                        slidesToScroll: 1,
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 479,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        })


        $('.features-slider-three').slick({
            speed: 5000,
            autoplay: true,
            autoplaySpeed: 0,
            cssEase: 'linear',
            slidesToShow: 6,
            slidesToScroll: 1,
            variableWidth: true,
            dots: false,
            arrows: false,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 4,
                        slidesToScroll: 1,
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 479,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        })
    }
    if ($('.case-studies-slider-one').length) {
        // case-slider slider
        $('.case-studies-slider-one').slick({
            speed: 500,
            autoplay: true,
            autoplaySpeed: 5000,
            infinite: true,
            slidesToShow: 4,
            slidesToScroll: 1,
            dots: true,
            arrows: true,
            arrows: false,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1,
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        })
    }
    if ($('.process-two-slider').length) {
        // process-two slider
        $('.process-two-slider').slick({
            speed: 500,
            autoplay: true,
            autoplaySpeed: 5000,
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
            variableWidth: true
        })
    }
    if ($('.case-studies-slider-two').length) {
        // case-studies slider
        $('.case-studies-slider-two').slick({
            speed: 500,
            autoplay: true,
            autoplaySpeed: 5000,
            infinite: true,
            slidesToShow: 2,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
            variableWidth: true,
            //centerMode: true,
        })
    }
    if ($('.testimonial-slider-one').length) {
        // testimonial-one slider
        $('.testimonial-slider-one').slick({
            speed: 500,
            autoplay: true,
            autoplaySpeed: 5000,
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
            arrows: false
        })
    }
    if ($('.testimonial-slider-three').length) {
        // testimonial-one slider
        $('.testimonial-slider-three').slick({
            speed: 500,
            autoplay: true,
            autoplaySpeed: 5000,
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: false,
            arrows: true,
            prevArrow: '<button type="button" class="slick-prev"><i class="flaticon-arrow-right"></i></button>',
            nextArrow: '<button type="button" class="slick-next"><i class="flaticon-arrow-right"></i></button>'
        })
    }
    if ($('.testimonial-slider-two').length) {
        // testimonial-two slider
        $('.testimonial-slider-two').slick({
            speed: 500,
            autoplay: true,
            autoplaySpeed: 50000,
            slidesToShow: 3,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
            responsive: [
                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1,
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        })
    }
    // wow animation
    if ($(".wow").length) {
        var wow = new WOW({
            boxClass: "wow",
            animateClass: "animated",
            mobile: true,
            live: true
        });
        wow.init();
    }
    if ($("#loan-calculator").length) {
        var monthRange = document.getElementById("range-slider-month");
        var countRange = document.getElementById("range-slider-count");

        var limitFieldMinMonth = document.getElementById("min-value-rangeslider-month");
        var limitFieldMaxMonth = document.getElementById("max-value-rangeslider-month");

        var limitFieldMinCount = document.getElementById("min-value-rangeslider-count");
        var limitFieldMaxCount = document.getElementById("max-value-rangeslider-count");

        noUiSlider.create(monthRange, {
            start: 6,
            behaviour: "snap",
            step: 1,
            tooltips: [
                wNumb({
                    decimals: 0,
                }),
            ],
            connect: [true, false],
            range: {
                min: 1,
                max: 12,
            },
        });

        noUiSlider.create(countRange, {
            start: 60000,
            step: 1000,
            tooltips: [
                wNumb({
                    decimals: 0,
                    prefix: "$",
                }),
            ],
            behaviour: "snap",
            connect: [true, false],
            range: {
                min: 10000,
                max: 100000,
            },
        });

        monthRange.noUiSlider.on("update", function (values, handle) {
            (handle ? $(limitFieldMaxMonth) : $(limitFieldMinMonth)).attr("value", values[handle]);
            let loanMoney = limitFieldMinCount.value;
            let interestRate = $("#loan-calculator").data("interest-rate");
            let interestRatePercent = parseInt(interestRate, 10) / 100;
            let totalPay = loanMoney * interestRatePercent + parseInt(loanMoney, 10);
            let monthlyPay = totalPay / parseInt(values[handle], 10);

            $("#loan-month").html(parseInt(values[handle], 10));
            $("#loan-monthly-pay").html(parseInt(monthlyPay, 10));
            $("#loan-total").html(parseInt(totalPay, 10));
        });

        countRange.noUiSlider.on("update", function (values, handle) {
            (handle ? $(limitFieldMaxCount) : $(limitFieldMinCount)).attr("value", values[handle]);

            let loanMonth = limitFieldMinMonth.value;
            let interestRate = $("#loan-calculator").data("interest-rate");
            let interestRatePercent = parseInt(interestRate, 10) / 100;
            let totalPay = values[handle] * interestRatePercent + parseInt(values[handle], 10);
            let monthlyPay = totalPay / parseInt(loanMonth, 10);

            $("#loan-month").html(parseInt(loanMonth, 10));
            $("#loan-monthly-pay").html(parseInt(monthlyPay, 10));
            $("#loan-total").html(parseInt(totalPay, 10));
        });

        let loanMoney = limitFieldMinCount.value;
        let loanMonth = limitFieldMinMonth.value;
        let interestRate = $("#loan-calculator").data("interest-rate");
        let interestRatePercent = parseInt(interestRate, 10) / 100;
        let totalPay = loanMoney * interestRatePercent + parseInt(loanMoney, 10);
        let monthlyPay = totalPay / parseInt(loanMonth, 10);

        $("#loan-month").html(parseInt(loanMonth, 10));
        $("#loan-monthly-pay").html(parseInt(monthlyPay, 10));
        $("#loan-total").html(parseInt(totalPay, 10));
    }

    if ($(".counter-box-one , .why-choose-three-counter").length) {
        var hasAnimated = false;

        function animateCounters() {
            $('.counter-box-one h6, .why-choose-three-counter h6').each(function () {
                var $this = $(this);
                var target = parseInt($this.data('target'), 10);
                var initial = 0;
                var symbol = $this.data('symbol') || '';

                $({ count: initial }).animate({ count: target }, {
                    duration: 2000,
                    step: function () {
                        $this.text(Math.floor(this.count) + symbol);
                    },
                    complete: function () {
                        $this.text(this.count + symbol);
                    }
                });
            });
        }
        function isInViewport(element) {
            var $element = $(element);
            var elementTop = $element.offset().top;
            var elementBottom = elementTop + $element.outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            return elementBottom > viewportTop && elementTop < viewportBottom;
        }
        $(window).on('scroll', function () {
            if (!hasAnimated && isInViewport('.counter-box-one , .why-choose-three-counter')) {
                animateCounters();
                hasAnimated = true;
            }
        });
        if (isInViewport('.counter-box-one, .why-choose-three-counter')) {
            animateCounters();
            hasAnimated = true;
        }
    }

    // video-popup
    if ($(".process-one-video, .testimonial-video-one, .features-video-info, .banner-three, .portfolio-detail-section").length) {
        $('.process-one-video-btn, .testimonial-video-btn-one, .features-video-btn-one , .about-three-video-btn, .portfolio-details-video-btn').YouTubePopUp();
    }

    if ($(".preloader").length) {
        //Preloader
        $(window).on('load', function () {
            if ($('.preloader').length) {
                $('.preloader').delay(2500).fadeOut(100);
            }
        });
    }

    // banner curved-circle
    function loan_cuved_circle() {
        let circleTypeElm = $(".curved-circle--item");
        if (circleTypeElm.length) {
            circleTypeElm.each(function () {
                let elm = $(this);
                let options = elm.data("circle-text-options");
                elm.circleType(
                    "object" === typeof options ? options : JSON.parse(options)
                );
            });
        }
    }

    $(window).on("load", function () {
        loan_cuved_circle();
    });



    if ($('.contact-form-inner , .apply-loan-section').length) {
        // filter section select option
        var $disabledResults = $(".loan-type, .from-dropdown");
        $disabledResults.select2();
    }

    // process bar
    if ($(".process-group").length) {
        $(".loan-process-inner").appear(
            function () {
                var el = $(this);
                var percent = el.data("percent");
                $(el).css("width", percent).addClass("counted");
            },
            {
                accY: -50
            }
        );
    }


    if ($('.portfolio-tabs').length) {
        // portfolio tab 
        document.addEventListener("DOMContentLoaded", function () {
            const allItemsContainer = document.getElementById('all-items');
            const businessItems = document.querySelectorAll('#business .portfolio-item');
            const homeItems = document.querySelectorAll('#home .portfolio-item');
            const personalItems = document.querySelectorAll('#personal .portfolio-item');
            const studentItems = document.querySelectorAll('#student .portfolio-item');

            function updateItemCount() {
                document.querySelector('.portfolio-tab-link[data-tab="all"] .item-count').textContent = homeItems.length + businessItems.length + personalItems.length + studentItems.length;
                document.querySelector('.portfolio-tab-link[data-tab="home"] .item-count').textContent = homeItems.length;
                document.querySelector('.portfolio-tab-link[data-tab="business"] .item-count').textContent = businessItems.length;
                document.querySelector('.portfolio-tab-link[data-tab="personal"] .item-count').textContent = personalItems.length;
                document.querySelector('.portfolio-tab-link[data-tab="student"] .item-count').textContent = studentItems.length;
            }

            businessItems.forEach(item => {
                allItemsContainer.appendChild(item.cloneNode(true));
            });

            homeItems.forEach(item => {
                allItemsContainer.appendChild(item.cloneNode(true));
            });
            personalItems.forEach(item => {
                allItemsContainer.appendChild(item.cloneNode(true));
            });
            studentItems.forEach(item => {
                allItemsContainer.appendChild(item.cloneNode(true));
            });

            updateItemCount();

            document.querySelectorAll('.portfolio-tab-link').forEach(link => {
                link.addEventListener('click', function () {
                    document.querySelectorAll('.portfolio-tab-link').forEach(link => link.classList.remove('active'));
                    document.querySelectorAll('.portfolio-tab-content').forEach(content => content.classList.remove('active'));

                    this.classList.add('active');
                    const tabId = this.getAttribute('data-tab');
                    document.getElementById(tabId).classList.add('active');
                });
            });
        });
    }

    if ($('.careers-tabs').length) {
        // portfolio tab 
        document.addEventListener("DOMContentLoaded", function () {
            const allItemscareers = document.getElementById('all-item');
            const officerItems = document.querySelectorAll('#officer .careers-tab-item');
            const analystItems = document.querySelectorAll('#analyst .careers-tab-item');
            const managerItems = document.querySelectorAll('#manager .careers-tab-item');
            const marketingItems = document.querySelectorAll('#marketing .careers-tab-item');

            function updateItemCounts() {
                document.querySelector('.careers-tab-link[data-tab="all"] .count-items').textContent = officerItems.length + analystItems.length + managerItems.length + marketingItems.length;
                document.querySelector('.careers-tab-link[data-tab="officer"] .count-items').textContent = officerItems.length;
                document.querySelector('.careers-tab-link[data-tab="analyst"] .count-items').textContent = analystItems.length;
                document.querySelector('.careers-tab-link[data-tab="manager"] .count-items').textContent = managerItems.length;
                document.querySelector('.careers-tab-link[data-tab="marketing"] .count-items').textContent = marketingItems.length;
            }

            officerItems.forEach(item => {
                allItemscareers.appendChild(item.cloneNode(true));
            });

            analystItems.forEach(item => {
                allItemscareers.appendChild(item.cloneNode(true));
            });
            managerItems.forEach(item => {
                allItemscareers.appendChild(item.cloneNode(true));
            });
            marketingItems.forEach(item => {
                allItemscareers.appendChild(item.cloneNode(true));
            });
            updateItemCounts();

            document.querySelectorAll('.careers-tab-link').forEach(link => {
                link.addEventListener('click', function () {
                    document.querySelectorAll('.careers-tab-link').forEach(link => link.classList.remove('active'));
                    document.querySelectorAll('.careers-tab-content').forEach(content => content.classList.remove('active'));

                    this.classList.add('active');
                    const tabId = this.getAttribute('data-tab');
                    document.getElementById(tabId).classList.add('active');
                });
            });
        });
    }

    if ($('.why-choose-section-one, .banner-three-video, .testimonial-three, .why-choose-section-one-2').length) {
        // why choose image animation effect
        window.addEventListener('scroll', function () {
            const elementsToAnimate = document.querySelectorAll('.why-choose-one-image img, .banner-three-video img , .testimonial-three .testimonial-three-background-image, .why-choose-one-image-2 img');

            elementsToAnimate.forEach((element) => {
                let winPos = window.pageYOffset;
                let targetPos = winPos * 0.05;
                element.style.transition = 'transform 0.8s ease-out';
                element.style.transform = `translateY(${targetPos}px) scale(1.2)`;
            });
        });
    }

    if ($('.heading-title').length) {
        const headings = document.querySelectorAll('.heading-title');
        const observerOptions = {
            root: null,
            threshold: 0.1
        };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const heading = entry.target;
                    const text = heading.textContent.replace(/\s+/g, ' ').trim();
                    heading.innerHTML = '';

                    const words = text.split(' ');

                    words.forEach((word, wordIndex) => {
                        const wordSpan = document.createElement('span');
                        wordSpan.style.display = 'inline-block';
                        heading.appendChild(wordSpan);

                        word.split('').forEach((letter, letterIndex) => {
                            const letterSpan = document.createElement('span');
                            letterSpan.textContent = letter;
                            wordSpan.appendChild(letterSpan);

                            letterSpan.style.opacity = 0;
                            letterSpan.style.transform = 'translateX(20px)';
                            letterSpan.style.transition = 'opacity 0.3s ease, transform 0.3s ease';

                            setTimeout(() => {
                                letterSpan.style.opacity = 1;
                                letterSpan.style.transform = 'translateX(0)';
                            }, (wordIndex * 400 + letterIndex * 40));
                        });


                        if (wordIndex < words.length - 1) {
                            const spaceSpan = document.createElement('span');
                            spaceSpan.textContent = ' ';
                            heading.appendChild(spaceSpan);
                        }

                        setTimeout(() => {
                            wordSpan.style.opacity = 1;
                        }, (wordIndex * 1000));
                    });

                    observer.unobserve(heading);
                }
            });
        }, observerOptions);

        headings.forEach(heading => {
            observer.observe(heading);
        });
    }





    $(document).ready(function () {
        if ($('.case-studies-one').length) {
            // Case study details
            $('.case-studies-one-details').each(function () {
                var $details = $(this).find(".case-studies-one__details");
                var elementHeight = $details.outerHeight() + 70;
                $details.css("margin-bottom", "-" + elementHeight + "px");
            });
        }
        if ($('.portfolio-one-item-inner').length) {
            // portfolio details
            $('.portfolio-one-item-inner').each(function () {
                var $lower = $(this).find(".portfolio-one-details-lower");
                var lowerheight = $lower.outerHeight();

                if (lowerheight === 0) {
                    $lower.css("margin-bottom", "-" + (lowerheight + 141) + "px");
                } else {
                    $lower.css("margin-bottom", "-" + lowerheight + "px");
                }
            });
        }
    });


    if ($('.case-studies-slider-one').length) {
        //bg image cheng
        $('.case-studies-slider-one-item').hover(function () {
            var imgSrc = $(this).find('.case-studies-one-image > img').attr('src');

            $('.case-studies-background').css('background-image', 'url(' + imgSrc + ')');
        });
    }

    $(window).on('scroll', function () {
        if ($('.process-one-image, .about-one-image, about-one_image, .why-choose-two-image, .about-two-image, .image-shape').length) {
            // active class add image effect
            $('.process-one-image, .about-one-image, .about-one_image,.why-choose-two-image, .about-two-image, .image-shape').each(function () {
                var elementTop = $(this).offset().top;
                var elementBottom = elementTop + $(this).outerHeight();
                var viewportTop = $(window).scrollTop();
                var viewportBottom = viewportTop + $(window).height();
                if (elementBottom > viewportTop && elementTop < viewportBottom) {
                    $(this).addClass('active');
                }
            });
        }
    });

    $(window).on('scroll', function () {
        // process-secound process-secound-info
        let currentVisible = null;
        $('.process-secound-info').each(function () {
            var offset = $(this).offset().top;

            if ($(window).scrollTop() + 600 >= offset) {
                currentVisible = $(this);
            }
        });

        $('.process-secound-box').each(function () {
            var boxClass = $(this).attr('class').split(' ').pop();

            if (currentVisible && boxClass === currentVisible.attr('data-first')) {
                $(this).css({
                    'opacity': 1,
                    'z-index': 1 
                });
            } else {
                $(this).css({
                    'opacity': 0,
                    'z-index': '' 
                });
            }
        });

        // Apply z-index to images based on the same logic (if needed for image layers)
        $('.process-secound-image img').each(function () {
            var imgClass = $(this).attr('class');

            if (currentVisible && imgClass && imgClass === currentVisible.attr('data-first')) {
                $(this).css('opacity', 1);
            } else {
                $(this).css('opacity', '0');
            }
        });
    });


    if ($('.case-studies-two-item').length) {
        //case studes active class add and remove
        $('.case-studies-two-item').click(function () {
            $('.case-studies-two-item').removeClass('active');

            $(this).addClass('active');
        });
    }

    if ($('.cta-two').length) {

    }
    /*-- Handle Scrollbar --*/
    function handleScrollbar() {
    const bodyHeight = $("body").height();
    const scrollPos = $(window).innerHeight() + $(window).scrollTop();
    let percentage = (scrollPos / bodyHeight) * 100;
    if (percentage > 100) {
        percentage = 100;
    }
    $(".scroll-to-top .scroll-to-top-inner").css("width", percentage + "%");
}

    $(window).on("scroll", function () {
        handleScrollbar();
    
        var scrollToTopBtn = ".scroll-to-top";
        if (scrollToTopBtn.length) {
          if ($(window).scrollTop() > 500) {
            $(scrollToTopBtn).addClass("show");
          } else {
            $(scrollToTopBtn).removeClass("show");
          }
        }
      });

})
    (window.jQuery);

if ($('#loan-chart').length) {
    // Loan details
    const loanAmount = 10000;
    const annualInterestRate = 0.08;
    const loanTermYears = 7;
    const months = loanTermYears * 12;
    const monthlyInterestRate = annualInterestRate / 12;

    // EMI Calculation
    const emi = loanAmount * (monthlyInterestRate * Math.pow(1 + monthlyInterestRate, months)) / (Math.pow(1 + monthlyInterestRate, months) - 1);

    // Breakdown of principal and interest paid each year
    const principalPaid = [1107.91, 1197.66, 1301.47, 1419.46, 1551.76];
    const interestPaid = [760.86, 670.11, 566.30, 448.31, 316.02];

    // Year labels
    const years = ['2024', '2025', '2026', '2027', '2028'];

    // Create the Highcharts chart
    Highcharts.chart('loan-chart', {
        chart: {
            type: 'column'
        },
        title: {
            text: ' '
        },
        series: [{
            name: 'Principal',
            data: principalPaid,
            color: '#F2F4F8'
        }, {
            name: 'Interest',
            data: interestPaid,
            color: '#09244C'
        }],
        xAxis: {
            categories: years,
            title: {
                text: 'Years'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Amount Paid ($)'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: 'gray'
                }
            }
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                // dataLabels: {
                //     enabled: true
                // }
            }
        }

    });
}



if ($('.cta-two').length) {
    let hasMoved = false;
    // cta text scroll efect
    $(window).on('scroll', function () {
        
        var scrollTop = $(this).scrollTop();
        var windowHeight = $(window).height();
        var elementOffset = $('.cta-two-box-one').offset().top;

        var distanceFromTop = elementOffset - scrollTop;

        var moveAmount = 400;

        if (distanceFromTop < windowHeight && distanceFromTop > -$('.cta-two-box-one').outerHeight()) {
            translateValue = Math.min(moveAmount, (windowHeight - distanceFromTop) / windowHeight * moveAmount);
            hasMoved = true;
        }

        if (hasMoved) {
            $('.cta-two-box-one').css('transform', 'translate(' + translateValue + 'px, 0px)');
        }
       
    });
    $(window).on('scroll', function () {
        var scrollTop = $(this).scrollTop();
        var windowHeight = $(window).height();
        var elementOffset = $('.cta-two-box-two').offset().top;

        var distanceFromTop = elementOffset - scrollTop;

        var moveAmount = 400;

        if (distanceFromTop < windowHeight && distanceFromTop > -$('.cta-two-box-two').outerHeight()) {
            translateValue = Math.min(moveAmount, (windowHeight - distanceFromTop) / windowHeight * moveAmount);
            hasMoved = true;
        }

        if (hasMoved) {
            $('.cta-two-box-two').css('transform', 'translate(' + -translateValue + 'px, 0px)');
        }
    });
}













