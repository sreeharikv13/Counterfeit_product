// Solidity program
// to store
// Employee Details
pragma solidity >=0.4.22 <0.9.0;

// Creating a Smart Contract
contract StructDemo{

// Structure of employee
struct product{
	// State variables
	uint bid;
	string product_name;
	string quantity;
	string mdate;
	string price;
	string expire_date;
	string image;
	uint mid;
}

product []emps;


// Function to add
// products details
function addProduct(uint bid, string memory product_name,string memory quantity,string memory mdate,string memory price,string memory expire_date,string memory image,uint mid) public{
	product memory e =product(bid, product_name,quantity,mdate,price,expire_date,image,mid);
	emps.push(e);
}

}
