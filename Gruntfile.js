module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        copy: {
            main: {
                files: [
                    { expand: true, cwd: 'node_modules/uikit/dist/css/', src: 'uikit.css', dest: 'app/static/css/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/dist/js/', src: 'uikit.js', dest: 'app/static/js/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/dist/js/', src: 'uikit-icons.js', dest: 'app/static/js/', filter: 'isFile' },
                ],
            },
        }
    });

    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('default', ['copy']);

};