<?php

/**
 * A script to dump php.ini settings to a csv.
 *
 * Usage:
 * php php_ini_dump.php
 */

/**
 * Output csv file name.
 */
define('PHP_INI_DUMP_OUT', 'php_ini_dump.csv');

main();

/**
 * Main function.
 */
function main() {
  $dumper = new PhpIniDumper(PHP_INI_DUMP_OUT);
  $dumper->loadPhpIniFlattened();
  $dumper->writeCsv();
  printf('php.ini settings are successfully dumped to `%s`.', PHP_INI_DUMP_OUT);
}

/**
 * A class which dumpes settings in php.ini
 */
class PhpIniDumper {

  /**
   * Csv file name.
   */
  private $filename;

  /**
   * Formatted data in php.ini.
   */
  private $phpIniRows;

  /**
   * Initializes an instance.
   */
  public function __construct($filename) {
    $this->filename = $filename;
  }

  /**
   * Loads php.ini in a flattened format.
   */
  public function loadPhpIniFlattened() {

    // Converts php.ini data into an indexed array.
    $php_ini_raw = ini_get_all();
    $this->phpIniRows = array_map(function ($key, $value) {
      $value_values = array_values($value);
      array_unshift($value_values, $key);
      return $value_values;
    }, array_keys($php_ini_raw), array_values($php_ini_raw));
    array_unshift($this->phpIniRows, [
      'name', 'global_value', 'local_value', 'access',
    ]);
  }

  /**
   * Writes to a csv file.
   */
  public function writeCsv() {
    try {
      $fp = fopen($this->filename, 'w');
      foreach ($this->phpIniRows as $row) {
        fputcsv($fp, $row);
      }
    } catch (Exception $e) {
      // TODO: Change this part if necessary.
      throw $e;
    } finally {
      fclose($fp);
    }
  }

}
