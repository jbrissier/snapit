
        $(document).ready(function(){
        $('#id_file, label').hide()

        $('#upload').click(function(){
                //choose file
                $('#id_file').click();

                return false;

            });

        });

        $('#id_file').change(function(){

                //submit form
                $('form').submit();


        });