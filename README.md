import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import './profile.css'; // Create this file for CSS

const ProfilePage = () => {
  const [activeSection, setActiveSection] = useState('profile');
  const [showAddressModal, setShowAddressModal] = useState(false);
  const [addresses, setAddresses] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    mobile: '',
    pincode: '',
    locality: '',
    city: '',
    state: '',
    address: '',
    landmark: '',
    alternatePhone: ''
  });

  const handleSectionChange = (section) => {
    setActiveSection(section);
  };

  const handleAddressSubmit = (e) => {
    e.preventDefault();
    setAddresses([...addresses, formData]);
    setShowAddressModal(false);
    setFormData({
      name: '',
      mobile: '',
      pincode: '',
      locality: '',
      city: '',
      state: '',
      address: '',
      landmark: '',
      alternatePhone: ''
    });
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    });
  };

  return (
    <section className="my-5">
      <div className="container">
        <div className="main-body">
          <div className="row">
            {/* Sidebar */}
            <div className="col-lg-4">
              <div className="card">
                <div className="card-body">
                  <ProfileSidebar 
                    activeSection={activeSection}
                    onSectionChange={handleSectionChange}
                  />
                </div>
              </div>
            </div>

            {/* Main Content */}
            <div className="col-lg-8">
              {activeSection === 'orders' && <OrderDetails />}
              {activeSection === 'profile' && <ProfileInformation />}
              {activeSection === 'address' && (
                <AddressBook 
                  addresses={addresses}
                  onAddAddress={() => setShowAddressModal(true)}
                />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Add Address Modal */}
      <AddAddressModal
        show={showAddressModal}
        onHide={() => setShowAddressModal(false)}
        onSubmit={handleAddressSubmit}
        formData={formData}
        onInputChange={handleInputChange}
      />
    </section>
  );
};

const ProfileSidebar = ({ activeSection, onSectionChange }) => (
  <div className="d-flex flex-column align-items-center text-center">
    <img 
      src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtbEsykx-0fhTred6UwHDYtMFd2UgTJCG4gaklT1dx4suRO4_n5LJr4Gg28kquSX5fpNo&usqp=CAU" 
      alt="Admin" 
      className="rounded-circle p-1 bg-warning" 
      width="110"
    />
    <div className="mt-3">
      <h4>Jyoti</h4>
      <p className="text-secondary mb-1">+91 7493658737</p>
      <p className="text-muted font-size-sm">Delhi, NCR</p>
    </div>
    <div className="list-group list-group-flush text-center mt-4">
      <a 
        href="#" 
        className={`list-group-item list-group-item-action border-0 ${activeSection === 'profile' ? 'active' : ''}`}
        onClick={() => onSectionChange('profile')}
      >
        Profile Information
      </a>
      <a 
        href="#" 
        className={`list-group-item list-group-item-action border-0 ${activeSection === 'orders' ? 'active' : ''}`}
        onClick={() => onSectionChange('orders')}
      >
        Orders
      </a>
      <a 
        href="#" 
        className={`list-group-item list-group-item-action border-0 ${activeSection === 'address' ? 'active' : ''}`}
        onClick={() => onSectionChange('address')}
      >
        Address Book
      </a>
      <a href="#" className="list-group-item list-group-item-action border-0">Logout</a>
    </div>
  </div>
);

const OrderDetails = () => (
  <div className="order_card">
    {/* Order Status and Product Details */}
    {/* Include your order timeline and product table here */}
  </div>
);

const ProfileInformation = () => (
  <div className="card">
    <div className="card-body">
      <div className="profile-info">
        <h5>Profile Information</h5>
        <p><strong>Name:</strong> Jyoti</p>
        <p><strong>Email Address:</strong> jyoti@gmail.com</p>
        {/* Add other profile fields */}
      </div>
    </div>
  </div>
);

const AddressBook = ({ addresses, onAddAddress }) => (
  <div className="card">
    <div className="card-body">
      <h5>Address Book</h5>
      <button className="add_address_button" onClick={onAddAddress}>
        Add Address
      </button>
      <div id="addressList">
        {addresses.map((address, index) => (
          <AddressItem key={index} address={address} />
        ))}
      </div>
    </div>
  </div>
);

const AddressItem = ({ address }) => (
  <div className="address-item">
    <p>{address.name}</p>
    <p>{address.address}</p>
    <p>{address.city}, {address.state} - {address.pincode}</p>
    {/* Add edit/delete buttons if needed */}
  </div>
);

const AddAddressModal = ({ show, onHide, onSubmit, formData, onInputChange }) => (
  <Modal show={show} onHide={onHide} centered>
    <Modal.Header closeButton>
      <Modal.Title>Add Address</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={onSubmit}>
        <div className="row">
          {/* Form fields with corresponding input elements */}
          <div className="col-md-6 mb-3">
            <label htmlFor="name">Name</label>
            <input 
              type="text" 
              className="form-control"
              id="name"
              value={formData.name}
              onChange={onInputChange}
              required
            />
          </div>
          {/* Add other form fields similarly */}
        </div>
        <div className="text-center">
          <Button variant="secondary" onClick={onHide} className="mr-2">
            Cancel
          </Button>
          <Button variant="primary" type="submit">
            Save Address
          </Button>
        </div>
      </form>
    </Modal.Body>
  </Modal>
);

export default ProfilePage;


npm install react-bootstrap bootstrap


import 'bootstrap/dist/css/bootstrap.min.css';


import ProfilePage from './components/ProfilePage';

function App() {
  return (
    <div className="App">
      <ProfilePage />
    </div>
  );
}
