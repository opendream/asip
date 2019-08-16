function cloneMore(selector, type) {

    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}



function url_slug(s, opt) {
	s = String(s);
	opt = Object(opt);

	var defaults = {
		'delimiter': '-',
		'limit': undefined,
		'lowercase': true,
		'replacements': {},
		'transliterate': (typeof(XRegExp) === 'undefined') ? true : false
	};

	// Merge options
	for (var k in defaults) {
		if (!opt.hasOwnProperty(k)) {
			opt[k] = defaults[k];
		}
	}

	var char_map = {
		// Latin
		'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE', 'Ç': 'C',
		'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
		'Ð': 'D', 'Ñ': 'N', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O', 'Ő': 'O',
		'Ø': 'O', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 'Ű': 'U', 'Ý': 'Y', 'Þ': 'TH',
		'ß': 'ss',
		'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c',
		'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
		'ð': 'd', 'ñ': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ő': 'o',
		'ø': 'o', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ű': 'u', 'ý': 'y', 'þ': 'th',
		'ÿ': 'y',

		// Latin symbols
		'©': '(c)',

		// Greek
		'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Θ': '8',
		'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': '3', 'Ο': 'O', 'Π': 'P',
		'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y', 'Φ': 'F', 'Χ': 'X', 'Ψ': 'PS', 'Ω': 'W',
		'Ά': 'A', 'Έ': 'E', 'Ί': 'I', 'Ό': 'O', 'Ύ': 'Y', 'Ή': 'H', 'Ώ': 'W', 'Ϊ': 'I',
		'Ϋ': 'Y',
		'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'h', 'θ': '8',
		'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': '3', 'ο': 'o', 'π': 'p',
		'ρ': 'r', 'σ': 's', 'τ': 't', 'υ': 'y', 'φ': 'f', 'χ': 'x', 'ψ': 'ps', 'ω': 'w',
		'ά': 'a', 'έ': 'e', 'ί': 'i', 'ό': 'o', 'ύ': 'y', 'ή': 'h', 'ώ': 'w', 'ς': 's',
		'ϊ': 'i', 'ΰ': 'y', 'ϋ': 'y', 'ΐ': 'i',

		// Turkish
		'Ş': 'S', 'İ': 'I', 'Ç': 'C', 'Ü': 'U', 'Ö': 'O', 'Ğ': 'G',
		'ş': 's', 'ı': 'i', 'ç': 'c', 'ü': 'u', 'ö': 'o', 'ğ': 'g',

		// Russian
		'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh',
		'З': 'Z', 'И': 'I', 'Й': 'J', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
		'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C',
		'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sh', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu',
		'Я': 'Ya',
		'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
		'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
		'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
		'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
		'я': 'ya',

		// Ukrainian
		'Є': 'Ye', 'І': 'I', 'Ї': 'Yi', 'Ґ': 'G',
		'є': 'ye', 'і': 'i', 'ї': 'yi', 'ґ': 'g',

		// Czech
		'Č': 'C', 'Ď': 'D', 'Ě': 'E', 'Ň': 'N', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ů': 'U',
		'Ž': 'Z',
		'č': 'c', 'ď': 'd', 'ě': 'e', 'ň': 'n', 'ř': 'r', 'š': 's', 'ť': 't', 'ů': 'u',
		'ž': 'z',

		// Polish
		'Ą': 'A', 'Ć': 'C', 'Ę': 'e', 'Ł': 'L', 'Ń': 'N', 'Ó': 'o', 'Ś': 'S', 'Ź': 'Z',
		'Ż': 'Z',
		'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z',
		'ż': 'z',

		// Latvian
		'Ā': 'A', 'Č': 'C', 'Ē': 'E', 'Ģ': 'G', 'Ī': 'i', 'Ķ': 'k', 'Ļ': 'L', 'Ņ': 'N',
		'Š': 'S', 'Ū': 'u', 'Ž': 'Z',
		'ā': 'a', 'č': 'c', 'ē': 'e', 'ģ': 'g', 'ī': 'i', 'ķ': 'k', 'ļ': 'l', 'ņ': 'n',
		'š': 's', 'ū': 'u', 'ž': 'z',

        // Thai
        // http://en.wikipedia.org/wiki/Royal_Thai_General_System_of_Transcription
        'ก': 'k',
        'ข': 'k', 'ฃ': 'k', 'ค': 'k', 'ฅ': 'k', 'ฆ': 'k',
        'ง': 'ng',
        'จ': 'ch',
        'ฉ': 'ch', 'ช': 'ch',
        'ซ': 's',
        'ฌ': 'ch',
        'ญ': 'y',
        'ฎ': 't',
        'ฏ': 't',
        'ฐ': 't', 'ฑ': 't', 'ฒ': 't',
        'ณ': 'n',
        'ด': 'd',
        'ต': 't',
        'ถ': 't', 'ท': 't', 'ธ': 't',
        'น': 'n',
        'บ': 'b',
        'ป': 'p',
        'ผ': 'ph',
        'ฝ': 'f',
        'พ': 'ph',
        'ฟ': 'f',
        'ภ': 'ph',
        'ม': 'm',
        'ย': 'y',
        'ร': 'r',
        'ฤ': 'rue',
        'ล': 'l',
        'ฦ': 'lue',
        'ว': 'w',
        'ศ': 's',
        'ษ': 's',
        'ส': 's',
        'ห': 'h',
        'ฬ': 'l',
        'อ': 'o',
        'ฮ': 'h',

        '่': '', '้': '', '๊': '', '๋': '', '็': '',
        'ะ': 'a', 'ั': 'a', 'า': 'a',
        'ำ': 'am',
        'ิ': 'i', 'ี': 'i',
        'ึ': 'ue', 'ื': 'ue',
        'ุ': 'u', 'ู': 'u',
        'เ': 'e',
        'แ': 'ae',
        'โ': 'o',
        'ใ': 'ai', 'ไ': 'ai'
	};

	// Make custom replacements
	for (var k in opt.replacements) {
		s = s.replace(RegExp(k, 'g'), opt.replacements[k]);
	}

	// Transliterate characters to ASCII
	if (opt.transliterate) {
		for (var k in char_map) {
			s = s.replace(RegExp(k, 'g'), char_map[k]);
		}
	}

	// Replace non-alphanumeric characters with our delimiter
	var alnum = (typeof(XRegExp) === 'undefined') ? RegExp('[^a-z0-9]+', 'ig') : XRegExp('[^\\p{L}\\p{N}]+', 'ig');
	s = s.replace(alnum, opt.delimiter);

	// Remove duplicate delimiters
	s = s.replace(RegExp('[' + opt.delimiter + ']{2,}', 'g'), opt.delimiter);

	// Truncate slug to max. characters
	s = s.substring(0, opt.limit);

	// Remove delimiter from ends
	s = s.replace(RegExp('(^' + opt.delimiter + '|' + opt.delimiter + '$)', 'g'), '');

	return opt.lowercase ? s.toLowerCase() : s;
}


function convertToSlug(text) {
    return text
        .toLowerCase()
        .replace(/ /g,'-')
        .replace(/[^\w-]+/g,'');
}


function controlPermalinkInline(selector, text) {
    if (text) {
        selector.parents('.permalink-inline').removeClass('permalink-hidden');
    }
    else {
        selector.parents('.permalink-inline').addClass('permalink-hidden');
    }
}


function generatePermalink() {
    var permalink = $('input[name=permalink], #id_permalink_readonly');
    if (permalink.val()) {
        return false;
    }

    var before_val = permalink.val();

    controlPermalinkInline(permalink, before_val);

    var selector = $('#generate-permalink input');

    selector.keyup(function() {

        if (permalink.hasClass('editing')) {
            return false;
        }

        var text = $(this).val();
        text = convertToSlug(url_slug($('<div>' + text + '</div>').text()));
        controlPermalinkInline(permalink, text);

        permalink.val(text).html(text);
    });

    selector.keyup();
}

function controlPermalink() {

    var edit_permalink = $('#edit-permalink');

    $(edit_permalink.attr('href')).hide();

    edit_permalink.click(function (e) {
        e.preventDefault();
        $(this).hide();
        $('#id_permalink_readonly').hide();
        $($(this).attr('href')).addClass('editing').show().focus().parents('.permalink-inline').removeClass('permalink-inline');

    });
}

function preventScrollReload() {
    $(window).on('beforeunload', function() {
        $(window).scrollTop(0);
    });
}

function checkTreeChange(input) {

    var li  = $(input).parents('li')
    var loop = true;

    while (loop) {

        li = li.next('li');
        var curr_label = li.find('label').eq(0);

        if (curr_label && curr_label.html() && (curr_label.html().indexOf('dlcorn;') > -1 ||  curr_label.html().indexOf('⌞') > -1)) {

            curr_label.parent().addClass('children-indent');

            if ($(input).prop('checked')) {
                li.slideDown('fast');
            }
            else {
                li.slideUp('fast');
                li.find('input').prop('checked', false);
                li.find('a').removeClass('checked');
            }
        }
        else {
            loop = false;
        }
    }
}


$(document).ready(function () {


    // checkbox radio style

    $('input[type=checkbox], input[type=radio]').each(function () {

        var label = $('label[for=' + $(this).attr('id') + ']');
        if (label && label.html() && label.html().indexOf('dlcorn;') == -1 && label.html().indexOf('⌞') == -1) {

            $(this).change(function () {
                checkTreeChange(this);
            });
            checkTreeChange(this);
        }
    });

    $('input[type="checkbox"][readonly]').on("click.readonly", function(event){event.preventDefault();}).css("opacity", "0.5");

    $('input[name=organization_primary_role]').change(function () {
        $('input[name=organization_roles]').each(function () {
            $(this).prop('readonly', false).get(0)
            .removeAttribute('onclick');
        });



            //.prop('disabled', false)
            //.siblings().removeClass('disabled');
        $('input[name=organization_roles]input[value='+$(this).val()+']')
            .prop('checked', true)
            .prop('readonly', true).get(0)
            .setAttribute('onclick', 'return false')

            //.prop('disabled', true)
            //.siblings()
            //    .addClass('checked')
            //    .addClass('disabled');


        $('input[name=organization_roles]').trigger('change');
    });

    $('input[name=organization_primary_role]:checked').trigger('change');


    $('input[name=organization_roles]').change(function () {

        if ($(this).prop('readonly')) {
            return false;
        }

        var depend_roles = '';
        $('.depend-on-role').hide()
        $('input[name=organization_roles]:checked').each(function() {
            $('.depend-on-role-id-' + this.value).show().removeClass('hide');
            depend_roles += '-' + this.value;
        });
        $('.depend-on-role-id-'+depend_roles).show().removeClass('hide');
    });
    $('input[name=organization_roles]').trigger('change');

    $('input[name=investor_type]').change(function () {

        if ($(this).prop('readonly')) {
            return false;
        }

        var depend_investor_type = '';
        $('.depend-on-investor_type').hide().addClass('hide');
        $('input[name=investor_type]:checked').each(function() {
            $('.depend-on-investor_type-id-' + this.value).show().removeClass('hide');
            depend_investor_type += '-' + this.value;
        });
        $('.depend-on-investor_type-id-'+depend_investor_type).show().removeClass('hide');
    });
    $('input[name=investor_type]').trigger('change');

    $('input[name=investment_stage_type]').change(function () {

        if ($(this).prop('readonly')) {
            return false;
        }

        var depend_investment_stage_type = '';
        $('.depend-on-investment_stage_type').hide().addClass('hide');
        $('input[name=investment_stage_type]:checked').each(function() {
            $('.depend-on-investment_stage_type-id-' + this.value).show().removeClass('hide');
            depend_investment_stage_type += '-' + this.value;
        });
        $('.depend-on-investment_stage_type-id-'+depend_investment_stage_type).show().removeClass('hide');
    });
    $('input[name=investment_stage_type]').trigger('change');

    $('input[name=specific_stage]').change(function () {

        if ($(this).prop('readonly')) {
            return false;
        }

        if (this.value) {
            $('.depend-on-specific_stage').show().removeClass('hide');
            $('.depend-on-specific_stage-render').html(this.value);
        } else {
            $('.depend-on-specific_stage').hide().addClass('hide');
        }
    });
    $('input[name=specific_stage]').trigger('change');

    $('input[name=kind]').change(function () {

        var depend_kinds = '';
        $('.depend-on-kind').hide().addClass('hide');
        $('input[name=kind]:checked').each(function() {
            $('.depend-on-kind-id-' + this.value).show().removeClass('hide');
            depend_kinds += '-' + this.value;
        });
        $('.depend-on-kind-id-'+depend_kinds).show().removeClass('hide');
    });
    $('input[name=kind]').trigger('change');

    $('.is-yes-depend input[type=radio], .is-yes-depend input[type=checkbox]').change(function () {

        console.log($(this).val(), $(this).prop('checked'));

        if ($(this).val() == 'True' && $(this).prop('checked')) {
            $('.is-yes-depend-on-' + $(this).attr('name')).show().removeClass('hide');
        } else {
            $('.is-yes-depend-on-' + $(this).attr('name')).hide().addClass('hide');
        }

    }).trigger('change');

    $('input[name=user_roles]').change(function (e) {

        var input = $(e.target);

        if (input.parent().hasClass('permalink-individual')) {
            if (input.prop('checked')) {
                $('.hide-on-individual').hide().addClass('hide');;
            }
            else {
                $('.hide-on-individual').show().removeClass('hide');
            }
        }

    });
    $('input[name=user_roles]').trigger('change');


    $('input[type=checkbox].select-with-other, input[type=radio].select-with-other').each(function () {
        var label = $('label[for=' + $(this).attr('id') + ']');
        var label_text = label.length && label.html().toLowerCase();

        if (label_text == 'other' || label_text == 'others') {
            $(this).change(function () {

                var other_id = $(this).attr('id')+'_other';

                if ($(this).prop('checked')) {
                    var parent = $(this).parent();
                    if (!parent.find('#' + other_id).length) {

                        var value = $(this).val();
                        var other_html = $('<input id="'+ other_id +'" class="input-other" type="text" value="' + value + '" />');

                        var option_element = $(this);
                        other_html.blur(function () {
                            option_element.val($(this).val());
                        });

                        parent.append(other_html)

                    }
                    else {
                        $('#' + other_id).show();
                    }
                }
                else {
                    $('#' + other_id).hide();
                }
            })
            $(this).change();
        }
    });

    $('.display-link-control').click(function (e) {
        e.preventDefault();
        var target_class = $(this).attr('href').replace('#', '');

        $('.display-on-' + target_class + '-click').show();
        $(this).remove();
    });

    // add more formset
    $('.add_more').click(function() {


        var selector = '#' + $(this).attr('id').replace('_add_more', '');
        var type = selector.replace('#id_', '')

        selector = selector + '>:last'

        var newElement = $(selector).clone(true);
        var total = $('#id_' + type + '-TOTAL_FORMS').val();
        newElement.find(':input').each(function() {
            var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        newElement.find('label').each(function() {
            var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
            $(this).attr('for', newFor);
        });
        total++;
        $('#id_' + type + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);

    });

    // confirm delete
    if ($('.btn-delete').length) {
        $('.btn-delete').popConfirm({
            title: "Delete Confirm",
            content: "Are you sure you want to delete <b>" + document.title.split('|')[0].replace('Edit', '') + "</b>?",
            placement: "top"
        });
    }

    $(document).bind('DOMNodeInserted', function(e) {
        var target = e.target;
        if ($(target).hasClass('btn-delete')) {
            $(target).popConfirm({
                title: "Delete Item",
                content: "Are you sure?",
                placement: "top"
            });
        }
    });

    // Editor fix top

    var nav_mergin_top = function (plus) {

        return function () {
            plus = plus || 0;
            var margin = $('.navbar-fixed-top').outerHeight() || 0;

            return margin + plus;
        }
    };


    // popup create link
    $('.popup-create-link, .popup-edit-link').click(function (e) {
        e.preventDefault();

        var wkey = $(this).attr('href').replace('/', '');

        window.open($(this).attr('href') + '?_popup=1', wkey, "width=auto,height=auto");

    });

    $(document).on('click', '.add-another-inline', function (e) {
      e.preventDefault();

      var href = $(this).attr('href');
      $('#' + $(this).attr('target')).load(encodeURI($(this).attr('href')));

    });


    /*
    if (typeof CKEDITOR != 'undefined') {

        var editor_fixtop = {};

        CKEDITOR.on( 'instanceReady', function( ev ) {

            $('.cke_top').each(function () {

                if (!editor_fixtop[$(this).attr('id')]) {

                    var calLimit = function () {

                        var container = $('.' + $(this).attr('id').replace('_top', ''));
                        var limit = container.offset().top + container.outerHeight() - 50;

                        return limit;
                    }

                    var options = {
                        marginTop: nav_mergin_top(0),
                        limit: calLimit,
                        removeOffsets: true
                    };

                    $(this).scrollToFixed(options);

                    editor_fixtop[$(this).attr('id')] = true;
                }
            });


        });
    };
    */

    /*
    $('.nav-stacked').scrollToFixed({
        marginTop: nav_mergin_top(30),
        limit: function () { return $('.main-content').height() - 298; },
        removeOffsets: true
    });
    */


    // Tab next
    var tab_stacked = $('form .nav-stacked');
    $('.btn-next').click(function (e) {
        e.preventDefault();
        var next_tab = $('li.active', tab_stacked).next();
        while (next_tab.hasClass('disabled') || next_tab.hasClass('hide')) {
            next_tab = next_tab.next();
        }

        next_tab.children('a').trigger('click');

        if (next_tab.next().length) {
        }
        else {
            $('.btn-submit').show();
            $(this).hide();
        }
        $('body').scrollTo('h1');

    });

    $('form a[data-toggle=tab]').click(function () {
        if ($(this).parent('li').next().length) {
            if ($(this).parent('li').hasClass('show-submit-button')) {
                $('.btn-submit').show();
            }
            else if ($(this).parent('li').hasClass('hide-submit-button')) {
                $('.btn-submit').hide();
            }
            else {
                $('.btn-submit').show();
            }
            $('.btn-next').show();
        }
        else {
            $('.btn-submit').show();
            $('.btn-next').hide();
        }
        $('html, body').animate({
            scrollTop: $("#tab_content").offset().top - 30
        }, 500);
    });


    // Dropdown
    $('.dropdown-menu').on('click', 'li a', function() {

        $('.text', $(this).parents('.dropdown')).text($(this).text());
    });

    // Active menu
    var basecamp_href = $('.breadcrumb a').eq(0).attr('href');

    $('a').filter(function() {

        var href = $(this).attr('href');

        if (!href) {
            return false;
        }

        if (document.location.pathname != '/' && ($.inArray(href, ['/', 'home', '#']) > -1)) {
            return false;
        }

        return document.location.pathname.indexOf(href) == 0 || (basecamp_href && basecamp_href.indexOf(href) == 0);

    }).addClass("active");

    // Flush submit check
    $('form').submit(function (e) {

        if (this.is_submitting) {
            e.preventDefault();
        }
        this.is_submitting = true;
    });

    // Menu toggle search
    var toggle_main_menu_class = function () {
        if ($("#block-search").hasClass('in')) {
            $('.navbar-main-menu').addClass('in')
        }
        else {
            $('.navbar-main-menu').removeClass('in')
        }
    };

    $("#block-search").bind('cssClassChanged', function(){
        toggle_main_menu_class()
    });
    toggle_main_menu_class();

    $('.top-menu-icon-search').click(function () {

        setTimeout(function () {
            $('#search-q').focus();
        }, 0)

    });


    // Form  and permalink
    var control_permalink = $('input[name=control_permalink]');
    control_permalink = parseInt(control_permalink.length && control_permalink.val());

    var prevent_scroll_reload = $('input[name=prevent_scroll_reload]');
    prevent_scroll_reload = parseInt(prevent_scroll_reload.length && prevent_scroll_reload.val());

    var is_new = $('input[name=is_new]');
    is_new = parseInt(is_new.length && is_new.val());

    if (control_permalink) {
        if (is_new) {
            generatePermalink();
        }
        controlPermalink();
    }
    if (prevent_scroll_reload) {
        preventScrollReload();
    }

    // Dirty check form
    $('form.dirty-check').areYouSure();
    $('.link-tooltip').tooltip();

    // stick-in-parent
    setTimeout(function () {
    //    $('.stick-in-parent').stick_in_parent();
        $('.form-sidebar-wrapper').stickem({offset: 20});
    }, 1000);


    // Point form
    if ($('.point-form').length && typeof POINT != 'undefined') {

        // Port from Python

        var pointMap = {};
        var pointDescriptionMap = {};

        var getPoint = function (updatePointDescriptionMap) {

            if (typeof POINT == 'undefined') {
                return 0;
            }

            var organization_primary_role = $('input[name=organization_primary_role]').val();
            var getPointMap = POINT[organization_primary_role];

            var maxTotal = 0;
            var total = 0;

            $.each(getPointMap, function (fieldName, point) {
                maxTotal += point;
            });

            if (maxTotal == 0) {
                return 0;
            }

            $.each(getPointMap, function (fieldName, point) {

                var value = null;

                // file widget
                if ($('[data-input-name=' + fieldName +']').length) {
                    value = $('[data-input-name=' + fieldName +'] .preview').length
                }

                // ckeditor
                else if (CKEDITOR.instances['id_' + fieldName]) {
                    value = CKEDITOR.instances['id_' + fieldName].getData()
                }

                // original input
                else if ($('[name=' + fieldName + ']').length) {

                    var element = $('[name=' + fieldName + ']');
                    if (element.attr('type') == 'checkbox') {
                        value = $('[name=' + fieldName + ']:checked').map(function(i, e) {  return $(e).val(); }).length;
                    }
                    else {
                        value = element.val()
                    }
                }

                if (typeof value == 'string') {
                    value = value.trim();
                }

                if (value) {
                    total += point;
                }

                if (updatePointDescriptionMap) {
                    pointDescriptionMap[fieldName] = Math.round(point/maxTotal*100);
                }
            });

            return Math.min(100, Math.ceil(total/maxTotal*100));
        };


        var updatePointDescription = function () {

            getPoint(true);

            var html = '<table class="tooltip-table"><thead><tr><th align="left">Field</th><th align="right">Percent</th></tr></thead><tbody>';
            $.each(pointDescriptionMap, function (fieldName, point) {

                var fieldLabel = $('label[for=id_' + fieldName + ']').text();
                html += '<tr><td align="left">' + fieldLabel + '</td><td align="right">' + point + '</td></tr>';
            });
            html += '</tbody></table>';

            $('.point-tooltip')
                .attr('title', html)
                .tooltip('destroy')
                .tooltip();


        };
        updatePointDescription();


        var updatePoint = function () {

            var percent = getPoint() + '%';
            $('.organization-percent-point .percent').css('width', percent);
            $('.organization-percent-point .text-percent').html(percent);

        };
        updatePoint();


        // Bind input change
        $.each(POINT, function (role, value) {
            $.extend(pointMap, value);
        });

        poinSelector = $.map(pointMap, function(element, index) {return '[name=' + index + ']'}).join(', ');

        $(poinSelector).change(function () {
            //console.log($(this).attr('name'), $(this).val());
            updatePoint();
        });

        $('.files-widget-dropbox').each(function () {
            var name = $(this).attr('data-input-name');
            if (pointMap[name]) {
                $(this).bind("DOMSubtreeModified",function(){
                    console.log($(this).attr('data-input-name'), $('.preview', $(this)).length);
                    updatePoint();
                });
            }

        });

        $.each(CKEDITOR.instances, function(index, instance) {
            var name = index.replace('id_', '');
            if (pointMap[name]) {
                instance.on('blur', function() {
                    //console.log(this.element.getAttribute('name'), this.getData());
                    updatePoint();
                })
            }
        });
    }


    // Update nav stack height
    var navStackedOriginalHeight = $('.stick-in-parent .nav-stacked').outerHeight();

    var updateHeightNavStacked = function () {

        var newHeight = $(window).height()-$('.organization-percent-point').height()-90;
        newHeight = Math.min(navStackedOriginalHeight, newHeight);
        $('.stick-in-parent .nav-stacked').height(newHeight);

        $('.tab-pane').css('min-height', $('.sidebar-left').height() -57);


    };
    updateHeightNavStacked();

    $(window).resize(updateHeightNavStacked);




    // Base modal
    var hide_modal_login = $('input[name=hide_modal_login]');
    hide_modal_login = parseInt(hide_modal_login.length && hide_modal_login.val());

    if (hide_modal_login) {
        $('a[data-target=#modal-login]').attr('href', "/account/login/");
    }


    var hide_modal_register = $('input[name=hide_modal_register]');
    hide_modal_register = parseInt(hide_modal_register.length && hide_modal_register.val());

    if (hide_modal_register) {
        $('a[data-target=#modal-register]').attr('href', "/account/register/");
    }


    var hide_modal_password_reset = $('input[name=hide_modal_password_reset]');
    hide_modal_password_reset = parseInt(hide_modal_password_reset.length && hide_modal_password_reset.val());

    if (hide_modal_password_reset) {
        $('a[data-target=#modal-password-reset]').attr('href', "/account/password_reset/");
    }


    // Management
    var update_order = function () {
        var item_length = $('tbody tr').length;

        $('.table-sortable tbody tr').each(function (i, item) {
            var input = $(item).find('input');
            if (input) {
                input.val(item_length-i);
            }
        });
        $('.table-sortable tbody').sortable({
            update: function(e, ui) {
                update_order();
                ui.item.addClass('changed');
            }
        });
    }
    update_order();

    // Hover edit
    $('.hover-edit').mouseover(function () {
        $('.menu-action-wrapper', this).css({display: 'inline'});
    }).mouseout(function () {
        $('.menu-action-wrapper', this).css({display: 'none'});
    })

    $('.create-profile__close').click(function () {
        var cp = $('.create-profile');
        cp.toggleClass('collapse-right');
        if (cp.hasClass('collapse-right')) {
            $(this).html('◄');
        } else {
            $(this).html('x');
        }
    })


    setTimeout(function () {
        $('[data-toggle="tooltip"]').tooltip();
    }, 3000);


    // slice
    setTimeout(function () {
        $('.btn-group.range .dropdown-menu').removeAttr("style");
    }, 2000);

});