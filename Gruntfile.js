module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        copy: {
            main: {
                files: [
                    { expand: true, cwd: 'node_modules/uikit/dist/js/', src: 'uikit.js', dest: 'assets/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/dist/js/', src: 'uikit-icons.js', dest: 'assets/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/src/scss/', src: '**', dest: 'resources/sass/uikit/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/src/js/', src: '**', dest: 'resources/js/uikit/', filter: 'isFile' },
                ],
            },
        },
        sass: {
            dist: {
                options: {
                    style: 'expanded'
                },
                files: {
                    'assets/app.css': 'resources/sass/app.scss'
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-sass');

    grunt.registerTask('default', ['copy', 'sass']);

};