
// read current files
$files = scandir($dir);
// remove . and ..
$files = array_diff($files, array('.', '..'));
// get all files with .txt extension
$files = preg_grep('/^([^.])*.txt$/', $files);