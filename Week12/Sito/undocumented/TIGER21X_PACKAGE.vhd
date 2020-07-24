library ieee;
use ieee.std_logic_1164.all;

package TIGER21X_PACKAGE is

	-----------------------------------------------------------------------------------
	-- ALU OPCODES 
	-----------------------------------------------------------------------------------
    constant ALU_ADD  : std_logic_vector(2 downto 0) := "000";
    constant ALU_MUL  : std_logic_vector(2 downto 0) := "001";
    constant ALU_EXP  : std_logic_vector(2 downto 0) := "010";
    constant ALU_SEQ  : std_logic_vector(2 downto 0) := "011";
    constant ALU_SLT  : std_logic_vector(2 downto 0) := "100";
    constant ALU_SGT  : std_logic_vector(2 downto 0) := "101";
	-- if any other, ALU output will be 0

end TIGER21X_PACKAGE;
