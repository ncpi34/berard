document.addEventListener('DOMContentLoaded', function(e) {
    const demoForm = document.getElementsByClassName('form');
    console.log('form', demoForm)

    // Get the submit button element
    const submitButton = demoForm.querySelector('[type="submit"]');

    FormValidation.formValidation(
        demoForm,
        {
            fields: {
                firstName: {
                    validators: {
                        notEmpty: {
                            message: 'The first name is required'
                        }
                    }
                },
                lastName: {
                    validators: {
                        notEmpty: {
                            message: 'The last name is required'
                        }
                    }
                },
                username: {
                    validators: {
                        notEmpty: {
                            message: 'The username is required'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: 'The username must be more than 6 and less than 30 characters long'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_]+$/,
                            message: 'The username can only consist of alphabetical, number and underscore'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: 'The email address is required'
                        },
                        emailAddress: {
                            message: 'The input is not a valid email address'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: 'The password is required'
                        },
                        stringLength: {
                            min: 8,
                            message: 'The password must have at least 8 characters'
                        },
                        different: {
                            message: 'The password cannot be the same as username',
                            compare: () => {
                                return demoForm.querySelector('[name="username"]').value;
                            }
                        }
                    }
                },
                gender: {
                    validators: {
                        notEmpty: {
                            message: 'The gender is required'
                        }
                    }
                },
                agree: {
                    validators: {
                        notEmpty: {
                            message: 'You must agree with the terms and conditions'
                        }
                    }
                },
            },
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                tachyons: new FormValidation.plugins.Tachyons(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
                fieldStatus: new FormValidation.plugins.FieldStatus({
                    onStatusChanged: function(areFieldsValid) {
                        if (areFieldsValid) {
                            // Enable the submit button
                            // so user has a chance to submit the form again
                            submitButton.removeAttribute('disabled');

                            // You can add more CSS classes to the submit button
                            submitButton.classList.add('bg-blue');
                            submitButton.classList.add('white');
                        } else {
                            // Disable the submit button
                            submitButton.setAttribute('disabled', 'disabled');
                            submitButton.classList.remove('bg-blue');
                            submitButton.classList.remove('white');
                        }
                    }
                }),
            },
        }
    );
});